# mcp_server.py
"""
MCP server that provides Canvas LMS integration capabilities.
This server exposes Canvas API functionality through MCP tools and resources.
"""

from mcp.server.fastmcp import FastMCP
from canvas_sdk import CanvasClient
from datetime import datetime, timezone, timedelta
import os
from typing import Optional, List, Dict, Any

# Initialize the MCP server
mcp = FastMCP("Canvas Course Assistant")

# Initialize Canvas client with environment variables
client = CanvasClient(
    api_token=os.getenv("CANVAS_TOKEN"),
    api_url=os.getenv("CANVAS_HOST")
)

def _validate_iso_date(date_str: str) -> datetime:
    """Validate and parse an ISO format date string.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        Parsed datetime object
        
    Raises:
        ValueError: If the date string is invalid or not in YYYY-MM-DD format
    """
    try:
        # First check if it matches YYYY-MM-DD format
        if len(date_str) != 10 or date_str[4] != '-' or date_str[7] != '-':
            raise ValueError(f"Date must be in YYYY-MM-DD format, got: {date_str}")
            
        # Try to parse it
        date = datetime.fromisoformat(date_str)
        return date
    except ValueError as e:
        raise ValueError(f"Invalid date format. Expected YYYY-MM-DD, got: {date_str}") from e

@mcp.tool()
def get_course_info(course_id: str) -> Dict[str, Any]:
    """Get information about a specific course."""
    try:
        return client.courses.get(course_id)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_active_courses(page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """Get a paginated list of active courses.
    
    Args:
        page: Page number to fetch
        per_page: Number of courses per page
    """
    try:
        return client.courses.list(
            state=['available'],
            page=page,
            per_page=per_page
        )
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_next_assignment(course_id: str) -> Dict[str, Any]:
    """Get the next upcoming assignment for a course.
    
    Args:
        course_id: The course ID to check
        
    Returns:
        Dict containing the next assignment's information or a message if none found
    """
    try:
        # Get course info first
        course = client.courses.get(course_id)
        
        # Get assignments with specific filters
        result = client.assignments.list(
            course_id,
            include=['due_at', 'submission'],
            page=1,
            per_page=1,  # We only need the next one
            order_by='due_at',
            bucket='upcoming'  # Only get upcoming assignments
        )
        
        # Check if we got any assignments
        assignments = result.get('assignments', [])
        if not assignments:
            return {"message": "No upcoming assignments"}
            
        # Get the first assignment (should be the next due)
        assignment = assignments[0]
        
        # Add course name to the assignment
        assignment['course_name'] = course.get('name', 'Unknown Course')
        
        return assignment
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_assignments_due_this_week(course_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get assignments due in the next 7 days.
    
    Args:
        course_id: Optional course ID to filter by
    """
    try:
        assignments = []
        if course_id:
            courses = [client.courses.get(course_id)]
        else:
            courses = client.courses.list(state=['available'])
            
        for course in courses:
            result = client.assignments.list(
                course['id'],
                include=['due_at', 'submission'],
                bucket='upcoming'
            )
            
            # Filter assignments due this week
            now = datetime.now(timezone.utc)
            week_end = now + timedelta(days=7)
            
            for assignment in result.get('assignments', []):
                if assignment.get('due_at'):
                    due_at = datetime.fromisoformat(assignment['due_at'].replace('Z', '+00:00'))
                    if due_at <= week_end:
                        assignment['course_name'] = course.get('name', 'Unknown Course')
                        assignments.append(assignment)
                
        return sorted(assignments, key=lambda x: x.get('due_at', ''))
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        return [{"error": str(e)}]

@mcp.tool()
def get_course_assignments(
    course_id: str,
    page: int = 1,
    per_page: int = 10,
    order_by: str = "due_at",
    bucket: Optional[str] = None
) -> Dict[str, Any]:
    """Get paginated assignments for a course.
    
    Args:
        course_id: The course ID
        page: Page number to fetch
        per_page: Number of assignments per page
        order_by: Field to order by (due_at, position, name)
        bucket: Filter by bucket (past, overdue, undated, ungraded, upcoming, future)
    """
    try:
        return client.assignments.list(
            course_id,
            include=['due_at', 'submission'],
            page=page,
            per_page=per_page,
            order_by=order_by,
            bucket=bucket
        )
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_assignments_by_date_range(
    start_date: str,
    end_date: str,
    course_id: Optional[str] = None,
    page: int = 1,
    per_page: int = 10
) -> List[Dict[str, Any]]:
    """Get assignments within a specific date range.
    
    Args:
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)
        course_id: Optional course ID to filter by
        page: Page number
        per_page: Items per page
        
    Returns:
        List of assignments within the date range
        
    Raises:
        ValueError: If the date format is invalid
    """
    try:
        # Validate and parse dates
        start = _validate_iso_date(start_date)
        end = _validate_iso_date(end_date)
        
        # Ensure start date is before end date
        if start > end:
            raise ValueError(f"Start date ({start_date}) must be before end date ({end_date})")
        
        assignments = []
        if course_id:
            courses = [client.courses.get(course_id)]
        else:
            courses = client.courses.list(state=['available'])
            
        for course in courses:
            course_assignments = client.assignments.get_assignments_by_date_range(
                course['id'],
                start,
                end,
                include=['due_at', 'submission'],
                page=page,
                per_page=per_page
            )
            
            for assignment in course_assignments:
                assignment['course_name'] = course.get('name', 'Unknown Course')
                assignments.append(assignment)
                
        return sorted(assignments, key=lambda x: x.get('due_at', ''))
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        return [{"error": str(e)}]

@mcp.prompt()
def course_summary_prompt(course_id: str) -> str:
    """Create a prompt for summarizing course information."""
    course = get_course_info(course_id)
    assignments = get_course_assignments(course_id, per_page=5, bucket='upcoming')
    
    if "error" in course:
        return f"Error: {course['error']}"
        
    prompt = f"""Please provide a summary of the course '{course.get('name', 'Unknown Course')}':
    
Course Information:
- Name: {course.get('name', 'Unknown')}
- Code: {course.get('course_code', 'Unknown')}
- Term: {course.get('term', {}).get('name', 'Unknown')}

Next 5 Upcoming Assignments:
"""
    
    if isinstance(assignments, dict) and "error" not in assignments:
        for assignment in assignments.get('assignments', []):
            prompt += f"- {assignment.get('name', 'Unknown')} (Due: {assignment.get('due_at', 'No due date')})\n"
            
    return prompt

if __name__ == "__main__":
    # Run the MCP server
    mcp.run() 