# examples/list_courses_with_due_dates.py
from canvas_sdk import CanvasClient
from datetime import datetime
import json

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

def main():
    # Create a client instance (will load from .env by default)
    client = CanvasClient()
    
    print("Fetching your courses...")
    # Get active courses
    courses = client.courses.list(
        state=['available'],
        include=['term']
    )
    
    if not courses:
        print("No active courses found.")
        return
    
    print(f"\nFound {len(courses)} active courses:\n")
    
    # Debug: Print the structure of the first course to understand its format
    if courses:
        first_course = courses[0]
        print("First course structure:")
        print(json.dumps(first_course, indent=2))
        
        # Check available keys
        print("\nAvailable keys in course object:")
        print(list(first_course.keys()))
    
    # For each course, get assignments with due dates
    for course in courses:
        # Use get() method to safely access keys that might not exist
        course_name = course.get('name', course.get('course_name', course.get('course_code', 'Unknown Course')))
        course_id = course.get('id')
        term_name = course.get('term', {}).get('name', 'No term')
        
        print(f"Course: {course_name}")
        print(f"Term: {term_name}")
        print(f"ID: {course_id}")
        
        # Ensure we have a valid course ID before proceeding
        if not course_id:
            print("  Invalid course ID, skipping...")
            continue
        
        # Get assignments for the course
        print("  Fetching assignments...")
        try:
            assignments = client.assignments.list(
                course_id,
                include=['due_at', 'submission']
            )
            
            # Sort assignments by due date
            assignments_with_due_dates = []
            assignments_without_due_dates = []
            
            for assignment in assignments:
                if assignment.get('due_at'):
                    assignments_with_due_dates.append(assignment)
                else:
                    assignments_without_due_dates.append(assignment)
            
            # Sort assignments with due dates by due date
            assignments_with_due_dates.sort(key=lambda x: x.get('due_at', ''))
            
            # Print upcoming assignments with due dates
            if assignments_with_due_dates:
                print("  Upcoming Assignments:")
                for assignment in assignments_with_due_dates:
                    name = assignment.get('name', 'Unnamed Assignment')
                    due_at = format_date(assignment.get('due_at'))
                    points = assignment.get('points_possible', 'N/A')
                    
                    # Check if assignment has been submitted
                    submission_status = "Not submitted"
                    if assignment.get('submission'):
                        if assignment['submission'].get('submitted_at'):
                            submission_status = "Submitted"
                        if assignment['submission'].get('graded_at'):
                            submission_status = "Graded"
                    
                    print(f"    - {name}")
                    print(f"      Due: {due_at}")
                    print(f"      Points: {points}")
                    print(f"      Status: {submission_status}")
                    print()
            else:
                print("  No assignments with due dates found.")
            
            # Show count of assignments without due dates
            if assignments_without_due_dates:
                print(f"  {len(assignments_without_due_dates)} assignments without due dates.")
            
        except Exception as e:
            print(f"  Error fetching assignments: {e}")
        
        print("-" * 80)
        print()

if __name__ == "__main__":
    main() 