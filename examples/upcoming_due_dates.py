# examples/upcoming_due_dates.py
from canvas_sdk import CanvasClient
from datetime import datetime, timezone
import json
import argparse

def format_date(date_str):
    """Format ISO date string to a more readable format.
    
    Args:
        date_str (str): ISO format date string
        
    Returns:
        str: Formatted date string
    """
    if not date_str:
        return "No due date"
    
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date_obj.strftime('%b %d, %Y at %I:%M %p')
    except (ValueError, AttributeError):
        return date_str

def parse_date(date_str):
    """Parse ISO date string to datetime object.
    
    Args:
        date_str (str): ISO format date string
        
    Returns:
        datetime: Datetime object or None if parsing fails
    """
    if not date_str:
        return None
    
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        return None

def get_course_info(client, course_id):
    """Get information about a specific course.
    
    Args:
        client (CanvasClient): Canvas API client
        course_id (str): Course ID to get information for
        
    Returns:
        dict: Course information or None if not found
    """
    try:
        return client.courses.get(course_id)
    except Exception as e:
        print(f"Error fetching course info: {e}")
        return None

def get_upcoming_assignments(client, course_id=None):
    """Get upcoming assignments for all courses or a specific course.
    
    Args:
        client (CanvasClient): Canvas API client
        course_id (str, optional): Specific course ID to get assignments for
        
    Returns:
        list: List of upcoming assignments
    """
    all_assignments = []
    now = datetime.now(timezone.utc)
    
    try:
        if course_id:
            # Get info for the specified course
            course = get_course_info(client, course_id)
            if not course:
                print(f"Course with ID {course_id} not found.")
                return []
                
            course_name = course.get('name', course.get('course_code', 'Unknown Course'))
            print(f"Fetching assignments for: {course_name} (ID: {course_id})")
            
            # Debug: Print course structure
            print("\nCourse structure:")
            print(json.dumps(course, indent=2))
            
            # Get assignments only for this course
            try:
                assignments = client.assignments.list(
                    course_id,
                    include=['due_at', 'submission']
                )
                
                # Add course info to each assignment
                for assignment in assignments:
                    assignment['course_name'] = course_name
                    assignment['course_id'] = course_id
                    
                    # Only include assignments with due dates in the future
                    due_at = parse_date(assignment.get('due_at'))
                    if due_at and due_at > now:
                        all_assignments.append(assignment)
                        
            except Exception as e:
                print(f"Error fetching assignments: {e}")
        else:
            # Get all active courses
            print("Fetching your active courses...")
            courses = client.courses.list(state=['available'])
            
            if not courses:
                print("No active courses found.")
                return []
                
            print(f"Found {len(courses)} active courses")
            
            # Get assignments from all courses
            for course in courses:
                # Safely get course info using get()
                course_name = course.get('name', course.get('course_name', course.get('course_code', 'Unknown Course')))
                course_id = course.get('id')
                
                if not course_id:
                    print(f"Skipping course with missing ID: {course_name}")
                    continue
                    
                print(f"Fetching assignments for: {course_name}")
                
                try:
                    assignments = client.assignments.list(
                        course_id,
                        include=['due_at', 'submission']
                    )
                    
                    # Add course info to each assignment
                    for assignment in assignments:
                        assignment['course_name'] = course_name
                        assignment['course_id'] = course_id
                        
                        # Only include assignments with due dates in the future
                        due_at = parse_date(assignment.get('due_at'))
                        if due_at and due_at > now:
                            all_assignments.append(assignment)
                            
                except Exception as e:
                    print(f"  Error fetching assignments: {e}")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
    # Sort all assignments by due date
    all_assignments.sort(key=lambda x: x.get('due_at', ''))
    return all_assignments

def display_upcoming_assignments(assignments):
    """Display upcoming assignments in a formatted way.
    
    Args:
        assignments (list): List of assignment objects
    """
    if not assignments:
        print("No upcoming assignments with due dates found.")
        return
    
    print(f"Found {len(assignments)} upcoming assignments:")
    print()
    
    # Group assignments by week
    current_week = None
    
    for assignment in assignments:
        due_at = parse_date(assignment.get('due_at'))
        if not due_at:
            continue
            
        assignment_week = due_at.strftime('%U') if due_at else None
        
        # Print week header if we're in a new week
        if assignment_week != current_week:
            current_week = assignment_week
            week_start = due_at.strftime('%b %d')
            print(f"\n--- Week of {week_start} ---\n")
        
        name = assignment.get('name', 'Unnamed Assignment')
        course_name = assignment.get('course_name', 'Unknown Course')
        formatted_due_date = format_date(assignment.get('due_at'))
        points = assignment.get('points_possible', 'N/A')
        
        # Check if assignment has been submitted
        submission_status = "Not submitted"
        if assignment.get('submission'):
            if assignment['submission'].get('submitted_at'):
                submission_status = "Submitted"
            if assignment['submission'].get('graded_at'):
                submission_status = "Graded"
        
        print(f"{formatted_due_date}")
        print(f"Course: {course_name}")
        print(f"Assignment: {name}")
        print(f"Points: {points}")
        print(f"Status: {submission_status}")
        print()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Show upcoming assignment due dates')
    parser.add_argument('--course', '-c', help='Specific course ID to show assignments for')
    args = parser.parse_args()
    
    # Create a client instance (will load from .env by default)
    client = CanvasClient()
    
    # If a course ID is provided, only show assignments for that course
    course_id = args.course
    
    if course_id:
        print(f"Checking upcoming due dates for course {course_id}...")
    else:
        print("Checking upcoming due dates across all courses...")
    
    # Get upcoming assignments
    assignments = get_upcoming_assignments(client, course_id)
    
    # Display header based on context
    if course_id:
        print(f"\n===== UPCOMING ASSIGNMENTS FOR COURSE {course_id} =====\n")
    else:
        print("\n===== UPCOMING ASSIGNMENTS ACROSS ALL COURSES =====\n")
    
    # Display assignments
    display_upcoming_assignments(assignments)

if __name__ == "__main__":
    main() 