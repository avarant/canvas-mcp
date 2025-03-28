# Canvas SDK Examples

This directory contains example scripts demonstrating how to use the Canvas SDK for common tasks.

## Prerequisites

Before running these examples, make sure you have:

1. Set up your `.env` file with your Canvas API token and institution URL:
```
CANVAS_TOKEN="your_canvas_api_token"
CANVAS_HOST="https://your-institution.instructure.com/"
```

2. Installed the required dependencies:
```bash
pip install -r ../requirements.txt
```

## Available Examples

### 1. List Courses with Due Dates

**File**: `list_courses_with_due_dates.py`

This script lists all your active courses along with assignments that have due dates for each course. It displays the course name, term, and a list of assignments with their due dates, point values, and submission status.

```bash
python examples/list_courses_with_due_dates.py
```

### 2. Upcoming Due Dates

**File**: `upcoming_due_dates.py`

This script focuses on upcoming assignments across all your courses or for a specific course. It only shows assignments with due dates in the future, sorted by date and grouped by week.

```bash
# Show upcoming due dates for all courses
python examples/upcoming_due_dates.py

# Show upcoming due dates for a specific course (replace 12345 with a course ID)
python examples/upcoming_due_dates.py --course 12345
# or use the short form
python examples/upcoming_due_dates.py -c 12345
```

You can find the course IDs by running the inspection tool: `python examples/inspect_canvas_api.py courses`

### 3. GraphQL Due Dates

**File**: `graphql_due_dates.py`

This script demonstrates how to use the Canvas GraphQL API to fetch courses and their assignments in a single request. The GraphQL API can be more efficient than making multiple REST API calls, especially for retrieving related data.

```bash
python examples/graphql_due_dates.py
```

### 4. API Structure Inspector

**File**: `inspect_canvas_api.py`

This diagnostic tool helps you explore the structure of Canvas API responses. It's useful for understanding the API's data format and debugging issues with the other examples.

```bash
# Inspect your user profile
python examples/inspect_canvas_api.py me

# List all courses and inspect the first one
python examples/inspect_canvas_api.py courses

# Inspect a specific course (replace 12345 with an actual course ID)
python examples/inspect_canvas_api.py courses --id 12345

# List assignments in a course (replace 12345 with an actual course ID)
python examples/inspect_canvas_api.py assignments --id 12345

# Test the GraphQL API (if available)
python examples/inspect_canvas_api.py test_graphql
```

This tool is particularly helpful when troubleshooting errors in other examples, as it shows the exact structure of API responses your Canvas instance provides.

## Troubleshooting

If you encounter `KeyError` exceptions in any of the examples, the API response structure from your Canvas instance might differ from what's expected. Use the inspection tool to understand the actual structure, then modify the examples accordingly.

Common issues:
- Canvas API responses may have different key names depending on the instance version
- Some fields that are expected may be missing or have a different format
- GraphQL API support varies by Canvas instance and may not be available

## Comparing REST and GraphQL Approaches

The examples demonstrate two different ways to access Canvas data:

1. **REST API** (used in the first two examples):
   - Makes multiple requests to different endpoints
   - Paginated responses for collections
   - More universal support
   - Simple to understand

2. **GraphQL API** (used in the third example):
   - Request exactly the data you need in a single query
   - Reduce data transfer and API calls
   - More efficient for complex related data
   - Requires Canvas instance with GraphQL support

## Customizing the Examples

Feel free to modify these examples to suit your needs. You might want to:

- Change the filtering criteria for courses or assignments
- Modify the output format for better readability
- Add export functionality to save results to CSV, JSON, etc.
- Create UI-based tools built on top of these examples 