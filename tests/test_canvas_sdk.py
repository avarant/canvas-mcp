# tests/test_canvas_sdk.py
"""
Unit tests for Canvas SDK assignments module.
"""

import pytest
from datetime import datetime, timezone
from canvas_sdk import CanvasClient
from canvas_sdk.resources.assignments import Assignments

# Sample API responses
SAMPLE_ASSIGNMENT = {
    "id": "123",
    "name": "Test Assignment",
    "due_at": "2024-03-28T23:59:59Z",
    "points_possible": 100,
    "course_id": "456"
}

SAMPLE_COURSE = {
    "id": "456",
    "name": "Test Course",
    "course_code": "TEST101",
    "term": {"name": "Spring 2024"}
}

@pytest.fixture
def mock_client(mocker):
    """Create a mock Canvas client."""
    client = mocker.Mock()
    client.get = mocker.Mock()
    client.post = mocker.Mock()
    client.put = mocker.Mock()
    client.delete = mocker.Mock()
    client.paginate = mocker.Mock()
    return client

@pytest.fixture
def assignments(mock_client):
    """Create an Assignments instance with a mock client."""
    return Assignments(mock_client)

def test_list_assignments(assignments, mock_client):
    """Test listing assignments with pagination."""
    # Setup mock response
    mock_client.paginate.return_value = [SAMPLE_ASSIGNMENT]
    
    # Call the method
    result = assignments.list("456", include=["due_at"])
    
    # Verify the call
    mock_client.paginate.assert_called_once()
    assert "courses/456/assignments" in mock_client.paginate.call_args[0][0]
    assert result == [SAMPLE_ASSIGNMENT]

def test_get_assignment(assignments, mock_client):
    """Test getting a single assignment."""
    # Setup mock response
    mock_client.get.return_value = SAMPLE_ASSIGNMENT
    
    # Call the method
    result = assignments.get("456", "123")
    
    # Verify the call
    mock_client.get.assert_called_once()
    assert "courses/456/assignments/123" in mock_client.get.call_args[0][0]
    assert result == SAMPLE_ASSIGNMENT

def test_create_assignment(assignments, mock_client):
    """Test creating an assignment."""
    # Setup mock response
    mock_client.post.return_value = SAMPLE_ASSIGNMENT
    
    # Call the method
    result = assignments.create("456", "Test Assignment", 100)
    
    # Verify the call
    mock_client.post.assert_called_once()
    assert "courses/456/assignments" in mock_client.post.call_args[0][0]
    assert result == SAMPLE_ASSIGNMENT

def test_update_assignment(assignments, mock_client):
    """Test updating an assignment."""
    # Setup mock response
    mock_client.put.return_value = SAMPLE_ASSIGNMENT
    
    # Call the method
    result = assignments.update("456", "123", json_data={"name": "Updated Assignment"})
    
    # Verify the call
    mock_client.put.assert_called_once()
    assert "courses/456/assignments/123" in mock_client.put.call_args[0][0]
    assert result == SAMPLE_ASSIGNMENT

def test_delete_assignment(assignments, mock_client):
    """Test deleting an assignment."""
    # Setup mock response
    mock_client.delete.return_value = SAMPLE_ASSIGNMENT
    
    # Call the method
    result = assignments.delete("456", "123")
    
    # Verify the call
    mock_client.delete.assert_called_once()
    assert "courses/456/assignments/123" in mock_client.delete.call_args[0][0]
    assert result == SAMPLE_ASSIGNMENT

def test_list_submissions(assignments, mock_client):
    """Test listing submissions for an assignment."""
    # Setup mock response
    sample_submission = {"id": "789", "user_id": "101", "grade": "A"}
    mock_client.paginate.return_value = [sample_submission]
    
    # Call the method
    result = assignments.list_submissions("456", "123")
    
    # Verify the call
    mock_client.paginate.assert_called_once()
    assert "courses/456/assignments/123/submissions" in mock_client.paginate.call_args[0][0]
    assert result == [sample_submission]

def test_get_submission(assignments, mock_client):
    """Test getting a submission for a user."""
    # Setup mock response
    sample_submission = {"id": "789", "user_id": "101", "grade": "A"}
    mock_client.get.return_value = sample_submission
    
    # Call the method
    result = assignments.get_submission("456", "123", "101")
    
    # Verify the call
    mock_client.get.assert_called_once()
    assert "courses/456/assignments/123/submissions/101" in mock_client.get.call_args[0][0]
    assert result == sample_submission

def test_update_submission(assignments, mock_client):
    """Test updating a submission."""
    # Setup mock response
    sample_submission = {"id": "789", "user_id": "101", "grade": "B"}
    mock_client.put.return_value = sample_submission
    
    # Call the method
    result = assignments.update_submission("456", "123", "101", json_data={"grade": "B"})
    
    # Verify the call
    mock_client.put.assert_called_once()
    assert "courses/456/assignments/123/submissions/101" in mock_client.put.call_args[0][0]
    assert result == sample_submission

def test_error_handling(assignments, mock_client):
    """Test error handling in assignments methods."""
    # Setup mock response to raise an exception
    mock_client.get.side_effect = Exception("API Error")
    
    # Verify that the exception is raised
    with pytest.raises(Exception) as exc_info:
        assignments.get("456", "123")
    assert str(exc_info.value) == "API Error" 