# examples/inspect_canvas_api.py
from canvas_sdk import CanvasClient
import json
import argparse

def inspect_rest_api(resource_type, item_id=None):
    """Inspect the structure of REST API responses.
    
    Args:
        resource_type (str): Type of resource to inspect ('courses', 'assignments', etc.)
        item_id (str, optional): Specific item ID to inspect
    """
    client = CanvasClient()
    
    try:
        if resource_type == 'me':
            # Get current user info
            data = client.users.get_self()
            print_structure("Current User", data)
            
        elif resource_type == 'courses':
            if item_id:
                # Get a specific course
                data = client.courses.get(item_id)
                print_structure(f"Course {item_id}", data)
            else:
                # Get list of courses
                data = client.courses.list(include=['term'])
                
                if not data:
                    print("No courses found.")
                    return
                
                print(f"Found {len(data)} courses.")
                
                # Print the first course as an example
                print_structure("First Course", data[0])
                
                # Print a list of course IDs and names for reference
                print("\nAll Courses:")
                for course in data:
                    name = course.get('name', course.get('course_code', 'Unknown'))
                    course_id = course.get('id', 'Unknown ID')
                    print(f"  - {name} (ID: {course_id})")
                
        elif resource_type == 'assignments':
            if not item_id:
                print("Error: Course ID required for assignments.")
                return
                
            # Get assignments for a course
            data = client.assignments.list(item_id)
            
            if not data:
                print(f"No assignments found for course {item_id}.")
                return
                
            print(f"Found {len(data)} assignments in course {item_id}.")
            
            # Print the first assignment as an example
            print_structure("First Assignment", data[0])
            
            # Print a list of assignment IDs and names for reference
            print("\nAll Assignments:")
            for assignment in data:
                name = assignment.get('name', 'Unnamed')
                assignment_id = assignment.get('id', 'Unknown ID')
                due_date = assignment.get('due_at', 'No due date')
                print(f"  - {name} (ID: {assignment_id}, Due: {due_date})")
                
        elif resource_type == 'modules':
            if not item_id:
                print("Error: Course ID required for modules.")
                return
                
            # Get modules for a course
            data = client.modules.list(item_id)
            
            if not data:
                print(f"No modules found for course {item_id}.")
                return
                
            print(f"Found {len(data)} modules in course {item_id}.")
            
            # Print the first module as an example
            print_structure("First Module", data[0])
            
        elif resource_type == 'test_graphql':
            # Test GraphQL API
            query = """
            {
              allCourses {
                _id
                name
              }
            }
            """
            
            data = client.graphql.query(query)
            print_structure("GraphQL Test Response", data)
            
        else:
            print(f"Unknown resource type: {resource_type}")
            print("Available types: me, courses, assignments, modules, test_graphql")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
def print_structure(label, data):
    """Print the structure of an API response.
    
    Args:
        label (str): Label for the data
        data (dict/list): Data to inspect
    """
    print(f"\n{'-' * 40}")
    print(f"{label}:")
    print(f"{'-' * 40}")
    
    # Print the full JSON structure
    print(json.dumps(data, indent=2))
    
    # If it's a dict, also print the keys at the top level
    if isinstance(data, dict):
        print("\nTop-level keys:")
        for key in data.keys():
            print(f"  - {key}")
    
    print(f"{'-' * 40}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Inspect Canvas API structure')
    parser.add_argument('resource', choices=['me', 'courses', 'assignments', 'modules', 'test_graphql'],
                        help='Resource type to inspect')
    parser.add_argument('--id', help='ID of the specific resource to inspect (e.g., course ID)')
    
    args = parser.parse_args()
    
    # Inspect the requested resource
    inspect_rest_api(args.resource, args.id)

if __name__ == "__main__":
    main() 