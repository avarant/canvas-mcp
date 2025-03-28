from .base import BaseResource
from typing import List, Dict, Any, Optional
from datetime import datetime

class Assignments(BaseResource):
    """Interface to the Canvas Assignments API."""
    
    def _get_item_id(self, item_id):
        """Convert item_id to string if needed."""
        return str(item_id) if item_id is not None else None

    def list(
        self,
        course_id: str,
        include: List[str] = None,
        page: int = None,
        per_page: int = None,
        order_by: str = None,
        bucket: str = None
    ) -> Dict[str, Any]:
        """List assignments with pagination support.
        
        Args:
            course_id: The course ID
            include: Additional fields to include
            page: Page number to fetch
            per_page: Number of items per page
            order_by: Field to order by (due_at, position, name)
            bucket: Filter by bucket (past, overdue, undated, ungraded, upcoming, future)
            
        Returns:
            Dict containing assignments and pagination info
        """
        course_id = self._get_item_id(course_id)
        params = {}
        
        if include:
            params["include[]"] = include
            
        if page is not None:
            params["page"] = page
            
        if per_page is not None:
            params["per_page"] = per_page
            
        if order_by:
            params["order_by"] = order_by
            
        if bucket:
            params["bucket"] = bucket
            
        assignments = list(self.client.paginate(
            f"courses/{course_id}/assignments",
            params=params
        ))
        
        return {"assignments": assignments}
    
    def get(self, course_id, assignment_id, include=None, **kwargs):
        """Get a single assignment.
        
        Args:
            course_id: The course ID
            assignment_id: The assignment ID
            include (list, optional): Additional information to include
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: Assignment object
        """
        course_id = self._get_item_id(course_id)
        assignment_id = self._get_item_id(assignment_id)
        
        params = kwargs.get('params', {})
        
        if include:
            params['include'] = include if isinstance(include, str) else ','.join(include)
            
        kwargs['params'] = params
        
        return self.client.get(f'courses/{course_id}/assignments/{assignment_id}', **kwargs)
    
    def create(self, course_id, name, points_possible, **kwargs):
        """Create a new assignment.
        
        Args:
            course_id: The course ID
            name (str): The name of the assignment
            points_possible (float): The maximum points possible for the assignment
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The created assignment
        """
        course_id = self._get_item_id(course_id)
        
        json_data = kwargs.get('json_data', {})
        json_data['assignment[name]'] = name
        json_data['assignment[points_possible]'] = points_possible
            
        kwargs['json_data'] = json_data
        
        return self.client.post(f'courses/{course_id}/assignments', **kwargs)
    
    def update(self, course_id, assignment_id, **kwargs):
        """Update an assignment.
        
        Args:
            course_id: The course ID
            assignment_id: The assignment ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The updated assignment
        """
        course_id = self._get_item_id(course_id)
        assignment_id = self._get_item_id(assignment_id)
        
        return self.client.put(f'courses/{course_id}/assignments/{assignment_id}', **kwargs)
    
    def delete(self, course_id, assignment_id, **kwargs):
        """Delete an assignment.
        
        Args:
            course_id: The course ID
            assignment_id: The assignment ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The deleted assignment
        """
        course_id = self._get_item_id(course_id)
        assignment_id = self._get_item_id(assignment_id)
        
        return self.client.delete(f'courses/{course_id}/assignments/{assignment_id}', **kwargs)
    
    def list_submissions(self, course_id, assignment_id, **kwargs):
        """List submissions for an assignment.
        
        Args:
            course_id: The course ID
            assignment_id: The assignment ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: List of submissions
        """
        course_id = self._get_item_id(course_id)
        assignment_id = self._get_item_id(assignment_id)
        
        return list(self.client.paginate(f'courses/{course_id}/assignments/{assignment_id}/submissions', **kwargs))
    
    def get_submission(self, course_id, assignment_id, user_id, **kwargs):
        """Get a submission for a user on an assignment.
        
        Args:
            course_id: The course ID
            assignment_id: The assignment ID
            user_id: The user ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: Submission object
        """
        course_id = self._get_item_id(course_id)
        assignment_id = self._get_item_id(assignment_id)
        user_id = self._get_item_id(user_id)
        
        return self.client.get(f'courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}', **kwargs)
    
    def update_submission(self, course_id, assignment_id, user_id, **kwargs):
        """Update a submission.
        
        Args:
            course_id: The course ID
            assignment_id: The assignment ID
            user_id: The user ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The updated submission
        """
        course_id = self._get_item_id(course_id)
        assignment_id = self._get_item_id(assignment_id)
        user_id = self._get_item_id(user_id)
        
        return self.client.put(f'courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}', **kwargs) 