# examples/graphql_due_dates.py
from canvas_sdk import CanvasClient
from datetime import datetime, timezone
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
    
    print("Fetching courses and assignments using GraphQL...")
    
    # Try a simpler query first to test GraphQL availability
    test_query = """
    {
      allCourses {
        _id
        name
      }
    }
    """
    
    try:
        # Test if GraphQL API is available
        test_result = client.graphql.query(test_query)
        
        if 'allCourses' not in test_result:
            print("GraphQL API doesn't seem to be available with current credentials.")
            print("Debug info:")
            print(json.dumps(test_result, indent=2))
            print("\nFalling back to REST API...")
            use_rest_api_fallback()
            return
            
        # Actual query with assignments
        query = """
        {
          allCourses {
            _id
            name
            term { name }
            assignmentsConnection(first: 100) {
              nodes {
                _id
                name
                dueAt
                pointsPossible
                needsGradingCount
              }
            }
          }
        }
        """
        
        result = client.graphql.query(query)
        
        if 'allCourses' not in result or not result['allCourses']:
            print("No courses found with GraphQL API.")
            return
        
        # Debug: Print the first course structure
        print("\nFirst course structure from GraphQL:")
        print(json.dumps(result['allCourses'][0], indent=2))
        
        courses = result['allCourses']
        print(f"\nFound {len(courses)} courses\n")
        
        now = datetime.now(timezone.utc)
        upcoming_assignments = []
        
        # Process courses and their assignments
        for course in courses:
            course_name = course.get('name', 'Unknown Course')
            course_id = course.get('_id')
            term_name = course.get('term', {}).get('name', 'No term')
            
            print(f"Course: {course_name}")
            print(f"Term: {term_name}")
            print(f"ID: {course_id}")
            
            assignments = course.get('assignmentsConnection', {}).get('nodes', [])
            future_assignments = []
            
            for assignment in assignments:
                due_at = assignment.get('dueAt')
                
                # Skip assignments without due dates
                if not due_at:
                    continue
                
                # Parse due date and check if it's in the future
                try:
                    due_date = datetime.fromisoformat(due_at.replace('Z', '+00:00'))
                    
                    if due_date > now:
                        # Add course info to assignment for later sorting
                        assignment['course_name'] = course_name
                        assignment['course_id'] = course_id
                        
                        # Add to both course-specific and overall lists
                        future_assignments.append(assignment)
                        upcoming_assignments.append(assignment)
                except (ValueError, AttributeError) as e:
                    print(f"  Error parsing date {due_at}: {e}")
            
            # Sort and display future assignments for this course
            if future_assignments:
                future_assignments.sort(key=lambda x: x.get('dueAt', ''))
                
                print(f"  Upcoming Assignments ({len(future_assignments)}):")
                for assignment in future_assignments:
                    name = assignment.get('name', 'Unnamed Assignment')
                    due_at = format_date(assignment.get('dueAt'))
                    points = assignment.get('pointsPossible', 'N/A')
                    
                    print(f"    - {name}")
                    print(f"      Due: {due_at}")
                    print(f"      Points: {points}")
                    print()
            else:
                print("  No upcoming assignments")
            
            print("-" * 80)
            print()
        
        # Display all upcoming assignments across all courses, sorted by due date
        if upcoming_assignments:
            upcoming_assignments.sort(key=lambda x: x.get('dueAt', ''))
            
            print("\n===== ALL UPCOMING ASSIGNMENTS =====\n")
            print(f"Total: {len(upcoming_assignments)} assignments")
            print()
            
            for assignment in upcoming_assignments:
                name = assignment.get('name', 'Unnamed Assignment')
                course_name = assignment.get('course_name', 'Unknown Course')
                due_at = format_date(assignment.get('dueAt'))
                points = assignment.get('pointsPossible', 'N/A')
                
                print(f"{due_at}")
                print(f"Course: {course_name}")
                print(f"Assignment: {name}")
                print(f"Points: {points}")
                print()
        
    except Exception as e:
        print(f"GraphQL query failed: {e}")
        print("Falling back to REST API...")
        use_rest_api_fallback()

def use_rest_api_fallback():
    """Use REST API as a fallback if GraphQL isn't available"""
    print("Using REST API instead of GraphQL...")
    
    try:
        # Import and run the upcoming_due_dates module which uses REST API
        import upcoming_due_dates
        upcoming_due_dates.main()
    except ImportError:
        print("Could not import upcoming_due_dates.py.")
        print("Please run 'python examples/upcoming_due_dates.py' instead.")
    except Exception as e:
        print(f"Error running REST API fallback: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 