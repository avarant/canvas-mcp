# canvas_sdk/resources/users.py
from .base import BaseResource

class Users(BaseResource):
    """Interface to the Canvas Users API."""
    
    def get_self(self, **kwargs):
        """Get the current user.
        
        Args:
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: User object for the current user
        """
        return self.client.get('users/self', **kwargs)
    
    def get(self, user_id, **kwargs):
        """Get a single user.
        
        Args:
            user_id: The user ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: User object
        """
        user_id = self._get_item_id(user_id)
        
        return self.client.get(f'users/{user_id}', **kwargs)
    
    def list_courses(self, user_id='self', **kwargs):
        """List courses for a user.
        
        Args:
            user_id: The user ID, defaults to 'self'
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: List of courses
        """
        user_id = self._get_item_id(user_id)
        
        return list(self.client.paginate(f'users/{user_id}/courses', **kwargs))
    
    def list_enrollments(self, user_id='self', **kwargs):
        """List enrollments for a user.
        
        Args:
            user_id: The user ID, defaults to 'self'
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: List of enrollments
        """
        user_id = self._get_item_id(user_id)
        
        return list(self.client.paginate(f'users/{user_id}/enrollments', **kwargs))
    
    def update(self, user_id, **kwargs):
        """Update a user.
        
        Args:
            user_id: The user ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The updated user
        """
        user_id = self._get_item_id(user_id)
        
        return self.client.put(f'users/{user_id}', **kwargs) 