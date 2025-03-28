# mcp_server.py
"""
MCP server that provides Canvas LMS integration capabilities.
This server exposes Canvas API functionality through MCP tools and resources.
"""

from mcp.server.fastmcp import FastMCP
from canvas_sdk import CanvasClient
from datetime import datetime, timezone
import os
from typing import Optional, List, Dict, Any

# Initialize the MCP server
mcp = FastMCP("Canvas Course Assistant")

# Initialize Canvas client with environment variables
client = CanvasClient(
    api_token=os.getenv("CANVAS_TOKEN"),
    api_url=os.getenv("CANVAS_HOST")
)

@mcp.tool()
def get_current_date() -> str:
    """Get the current date.
    
    Returns:
        The current date in the format YYYY-MM-DD.
    """
    return datetime.now().strftime("%Y-%m-%d")

@mcp.tool()
def get_course_info(course_id: str) -> Dict[str, Any]:
    """Get information about a specific course.
    
    Args:
        course_id (str): The ID of the course to get information for
        
    Returns:
        Dict containing course information including name, code, term, etc.
        If there's an error, returns a dict with an 'error' key.
    """
    try:
        return client.courses.get(course_id)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_active_courses() -> List[Dict[str, Any]]:
    """Get a list of all active courses.
    
    Returns:
        List of course information dictionaries.
        Each dict contains course details like name, code, term, etc.
        If there's an error, returns a list with a single dict containing an 'error' key.
    """
    try:
        return client.courses.list(state=['available'])
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def get_course_assignments(course_id: str) -> List[Dict[str, Any]]:
    """Get all assignments for a specific course.
    
    Args:
        course_id (str): The ID of the course to get assignments for
        
    Returns:
        List of assignment information dictionaries.
        Each dict contains assignment details like name, due date, submission info.
        If there's an error, returns a list with a single dict containing an 'error' key.
    """
    try:
        return client.assignments.list(course_id, include=['due_at', 'submission'])
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def get_upcoming_assignments(course_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get upcoming assignments for all courses or a specific course.
    
    Args:
        course_id (Optional[str]): Specific course ID to get assignments for.
                                 If None, returns upcoming assignments for all courses.
        
    Returns:
        List of upcoming assignment information dictionaries.
        Each dict contains assignment details and the course name.
        Assignments are sorted by due date.
        If there's an error, returns a list with a single dict containing an 'error' key.
    """
    now = datetime.now(timezone.utc)
    assignments = []
    
    try:
        if course_id:
            courses = [client.courses.get(course_id)]
        else:
            courses = client.courses.list(state=['available'])
            
        for course in courses:
            course_assignments = client.assignments.list(
                course['id'],
                include=['due_at', 'submission']
            )
            
            for assignment in course_assignments:
                if assignment.get('due_at'):
                    due_at = datetime.fromisoformat(assignment['due_at'].replace('Z', '+00:00'))
                    if due_at > now:
                        assignment['course_name'] = course.get('name', 'Unknown Course')
                        assignments.append(assignment)
                        
        return sorted(assignments, key=lambda x: x.get('due_at', ''))
    except Exception as e:
        return [{"error": str(e)}]

@mcp.prompt()
def course_summary_prompt(course_id: str) -> str:
    """Create a prompt for summarizing course information.
    
    Args:
        course_id (str): The ID of the course to summarize
        
    Returns:
        Formatted prompt string containing course information and assignments.
        If there's an error, returns an error message.
    """
    course = get_course_info(course_id)
    assignments = get_course_assignments(course_id)
    
    if "error" in course:
        return f"Error: {course['error']}"
        
    prompt = f"""Please provide a summary of the course '{course.get('name', 'Unknown Course')}':
    
Course Information:
- Name: {course.get('name', 'Unknown')}
- Code: {course.get('course_code', 'Unknown')}
- Term: {course.get('term', {}).get('name', 'Unknown')}

Assignments:
"""
    
    for assignment in assignments:
        if "error" not in assignment:
            prompt += f"- {assignment.get('name', 'Unknown')} (Due: {assignment.get('due_at', 'No due date')})\n"
            
    return prompt

if __name__ == "__main__":
    # Run the MCP server
    mcp.run() 