# Canvas MCP Server

This MCP server provides Canvas LMS integration capabilities through the Model Context Protocol. It allows LLMs to interact with your Canvas courses, assignments, and other course-related information.

## Features

- Get course information
- List active courses
- Get course assignments
- Get upcoming assignments
- Generate course summaries

## Prerequisites

1. Python 3.7 or higher
2. Canvas API access token
3. Canvas instance URL

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your Canvas credentials:
```
CANVAS_TOKEN="your_canvas_api_token"
CANVAS_HOST="https://your-institution.instructure.com/"
```

Note: The environment variables `CANVAS_TOKEN` and `CANVAS_HOST` correspond to the `api_token` and `api_url` parameters in the CanvasClient.

## Running the Server

To start the MCP server:

```bash
python mcp_server.py
```

## Using with Cursor

1. Start the MCP server as described above
2. Open Cursor
3. The MCP server will automatically connect to Cursor
4. You can now ask questions about your Canvas courses

## Example Queries

You can ask questions like:
- "What are my upcoming assignments?"
- "Tell me about course 12345"
- "List all my active courses"
- "What assignments are due next week in course 12345?"

## Available Tools

The server provides these main tools:

- `get_course_info`: Get details about a specific course
- `list_active_courses`: Get all your active courses
- `get_course_assignments`: Get assignments for a specific course
- `get_upcoming_assignments`: Get upcoming assignments (all courses or specific course)
- `course_summary_prompt`: Generate a summary of a course

## Error Handling

The server handles errors gracefully and provides clear error messages when:
- A course is not found
- API calls fail
- Required data is missing
- Authentication fails

## Security

- Canvas API credentials are loaded from environment variables
- No credentials are stored in the code
- All API calls are made over HTTPS 