"""
Unit tests for MCP server tools.
"""

import os
import sys
import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mcp_server

# Sample API responses
SAMPLE_COURSE = {
    "id": "456",
    "name": "Test Course",
    "course_code": "TEST101",
    "term": {"name": "Spring 2024"}
}

SAMPLE_ASSIGNMENT = {
    "id": "123",
    "name": "Test Assignment",
    "due_at": "2024-03-28T23:59:59Z",
    "points_possible": 100,
    "course_id": "456"
}

@pytest.fixture
def mock_canvas_client(mocker):
    """Create a mock Canvas client with all necessary methods."""
    client = mocker.Mock()
    
    # Mock courses
    client.courses = mocker.Mock()
    client.courses.get = mocker.Mock(return_value=SAMPLE_COURSE)
    client.courses.list = mocker.Mock(return_value=[SAMPLE_COURSE])
    
    # Mock assignments
    client.assignments = mocker.Mock()
    client.assignments.list = mocker.Mock(return_value=[SAMPLE_ASSIGNMENT])
    client.assignments.get = mocker.Mock(return_value=SAMPLE_ASSIGNMENT)
    
    return client

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables."""
    monkeypatch.setenv("CANVAS_TOKEN", "test_token")
    monkeypatch.setenv("CANVAS_HOST", "https://test.instructure.com")

def test_get_course_info(mock_canvas_client):
    """Test getting course information."""
    with patch('mcp_server.client', mock_canvas_client):
        result = mcp_server.get_course_info("456")
        assert result == SAMPLE_COURSE
        mock_canvas_client.courses.get.assert_called_once_with("456")

def test_list_active_courses(mock_canvas_client):
    """Test listing active courses with pagination."""
    with patch('mcp_server.client', mock_canvas_client):
        result = mcp_server.list_active_courses(page=1, per_page=10)
        mock_canvas_client.courses.list.assert_called_once_with(
            state=['available'],
            page=1,
            per_page=10
        )

def test_get_next_assignment(mock_canvas_client):
    """Test getting the next assignment."""
    # Mock the assignments list response
    mock_canvas_client.assignments.list.return_value = {
        'assignments': [SAMPLE_ASSIGNMENT]
    }
    
    with patch('mcp_server.client', mock_canvas_client):
        result = mcp_server.get_next_assignment("456")
        
        # Verify the result
        assert result.get('course_name') == SAMPLE_COURSE['name']
        assert result.get('name') == SAMPLE_ASSIGNMENT['name']
        assert result.get('due_at') == SAMPLE_ASSIGNMENT['due_at']
        
        # Verify the call parameters
        mock_canvas_client.assignments.list.assert_called_once_with(
            "456",
            include=['due_at', 'submission'],
            page=1,
            per_page=1,
            order_by='due_at',
            bucket='upcoming'
        )

def test_get_next_assignment_no_assignments(mock_canvas_client):
    """Test getting the next assignment when there are none."""
    # Mock empty assignments list
    mock_canvas_client.assignments.list.return_value = {
        'assignments': []
    }
    
    with patch('mcp_server.client', mock_canvas_client):
        result = mcp_server.get_next_assignment("456")
        assert result == {"message": "No upcoming assignments"}

def test_get_next_assignment_error(mock_canvas_client):
    """Test getting the next assignment when an error occurs."""
    # Make the client raise an exception
    mock_canvas_client.assignments.list.side_effect = Exception("API Error")
    
    with patch('mcp_server.client', mock_canvas_client):
        result = mcp_server.get_next_assignment("456")
        assert result == {"error": "API Error"}

def test_get_assignments_due_this_week(mock_canvas_client):
    """Test getting assignments due this week."""
    # Mock the assignments list response
    mock_canvas_client.assignments.list.return_value = {
        'assignments': [SAMPLE_ASSIGNMENT]
    }
    
    with patch('mcp_server.client', mock_canvas_client):
        result = mcp_server.get_assignments_due_this_week("456")
        assert len(result) == 1
        assert result[0].get('course_name') == SAMPLE_COURSE['name']
        
        # Verify the call parameters
        mock_canvas_client.assignments.list.assert_called_with(
            "456",
            include=['due_at', 'submission'],
            bucket='upcoming'
        )

def test_get_assignments_due_this_week_no_assignments(mock_canvas_client):
    """Test getting assignments due this week when there are none."""
    # Mock empty assignments list
    mock_canvas_client.assignments.list.return_value = {
        'assignments': []
    }
    
    with patch('mcp_server.client', mock_canvas_client):
        result = mcp_server.get_assignments_due_this_week("456")
        assert len(result) == 0

def test_get_assignments_due_this_week_error(mock_canvas_client):
    """Test getting assignments due this week when an error occurs."""
    # Make the client raise an exception
    mock_canvas_client.assignments.list.side_effect = Exception("API Error")
    
    with patch('mcp_server.client', mock_canvas_client):
        result = mcp_server.get_assignments_due_this_week("456")
        assert len(result) == 1
        assert result[0].get('error') == "API Error"

def test_get_course_assignments(mock_canvas_client):
    """Test getting course assignments with pagination and filtering."""
    with patch('mcp_server.client', mock_canvas_client):
        result = mcp_server.get_course_assignments(
            "456",
            page=1,
            per_page=10,
            order_by="due_at",
            bucket="upcoming"
        )
        mock_canvas_client.assignments.list.assert_called_once_with(
            "456",
            include=['due_at', 'submission'],
            page=1,
            per_page=10,
            order_by="due_at",
            bucket="upcoming"
        )

def test_get_assignments_by_date_range(mock_canvas_client):
    """Test getting assignments within a date range."""
    with patch('mcp_server.client', mock_canvas_client):
        # Test with various invalid date formats
        invalid_dates = [
            "invalid_date",          # Completely invalid
            "2024/03/31",           # Wrong separator
            "2024-3-31",            # Missing leading zero
            "24-03-31",             # Two-digit year
            "2024-03",              # Missing day
            "2024-13-31",           # Invalid month
            "2024-03-32",           # Invalid day
        ]
        
        for invalid_date in invalid_dates:
            with pytest.raises(ValueError) as exc_info:
                mcp_server.get_assignments_by_date_range(
                    invalid_date,
                    "2024-03-31"
                )
            assert "Invalid date format" in str(exc_info.value) or "Date must be in YYYY-MM-DD format" in str(exc_info.value)
            
            with pytest.raises(ValueError) as exc_info:
                mcp_server.get_assignments_by_date_range(
                    "2024-03-01",
                    invalid_date
                )
            assert "Invalid date format" in str(exc_info.value) or "Date must be in YYYY-MM-DD format" in str(exc_info.value)
        
        # Test with end date before start date
        with pytest.raises(ValueError) as exc_info:
            mcp_server.get_assignments_by_date_range(
                "2024-03-31",
                "2024-03-01"
            )
        assert "Start date" in str(exc_info.value) and "must be before end date" in str(exc_info.value)
        
        # Test with valid dates
        result = mcp_server.get_assignments_by_date_range(
            "2024-03-01",
            "2024-03-31"
        )
        assert isinstance(result, list)

def test_date_validation_helper():
    """Test the _validate_iso_date helper function directly."""
    # Test valid date
    date = mcp_server._validate_iso_date("2024-03-31")
    assert isinstance(date, datetime)
    assert date.year == 2024
    assert date.month == 3
    assert date.day == 31
    
    # Test invalid formats
    with pytest.raises(ValueError):
        mcp_server._validate_iso_date("2024/03/31")
    
    with pytest.raises(ValueError):
        mcp_server._validate_iso_date("2024-3-31")
    
    with pytest.raises(ValueError):
        mcp_server._validate_iso_date("invalid")

def test_course_summary_prompt(mock_canvas_client):
    """Test generating a course summary prompt."""
    # Mock the assignments list response
    mock_canvas_client.assignments.list.return_value = {
        'assignments': [SAMPLE_ASSIGNMENT]
    }
    
    with patch('mcp_server.client', mock_canvas_client):
        result = mcp_server.course_summary_prompt("456")
        assert "Test Course" in result
        assert "Test Assignment" in result
        assert "2024-03-28" in result

def test_error_handling(mock_canvas_client):
    """Test error handling in MCP tools."""
    # Make the client raise an exception
    mock_canvas_client.courses.get.side_effect = Exception("API Error")
    
    with patch('mcp_server.client', mock_canvas_client):
        result = mcp_server.get_course_info("456")
        assert "error" in result
        assert result["error"] == "API Error" 