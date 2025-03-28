# canvas_sdk/resources/courses.py
from .base import BaseResource

class Courses(BaseResource):
    """Interface to the Canvas Courses API."""
    
    def list(self, enrollment_type=None, enrollment_role=None, include=None, state=None, **kwargs):
        """List courses the user is enrolled in.
        
        Args:
            enrollment_type (str, optional): Filter by enrollment type (e.g., 'teacher', 'student')
            enrollment_role (str, optional): Filter by enrollment role
            include (list, optional): Additional information to include ('term', 'total_students', etc.)
            state (list, optional): Filter by course state ('available', 'completed', 'unpublished')
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: List of courses
        """
        params = kwargs.get('params', {})
        
        if enrollment_type:
            params['enrollment_type'] = enrollment_type
        if enrollment_role:
            params['enrollment_role'] = enrollment_role
        if include:
            params['include'] = include if isinstance(include, str) else ','.join(include)
        if state:
            params['state'] = state if isinstance(state, str) else ','.join(state)
            
        kwargs['params'] = params
        
        return list(self.client.paginate('courses', **kwargs))
    
    def get(self, course_id, include=None, **kwargs):
        """Get a single course.
        
        Args:
            course_id: The course ID
            include (list, optional): Additional information to include
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: Course object
        """
        course_id = self._get_item_id(course_id)
        
        params = kwargs.get('params', {})
        
        if include:
            params['include'] = include if isinstance(include, str) else ','.join(include)
            
        kwargs['params'] = params
        
        return self.client.get(f'courses/{course_id}', **kwargs)
    
    def create(self, name, course_code=None, **kwargs):
        """Create a new course.
        
        Args:
            name (str): The name of the course
            course_code (str, optional): The course code
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The created course
        """
        json_data = kwargs.get('json_data', {})
        
        json_data['course[name]'] = name
        if course_code:
            json_data['course[course_code]'] = course_code
            
        kwargs['json_data'] = json_data
        
        return self.client.post('courses', **kwargs)
    
    def update(self, course_id, **kwargs):
        """Update a course.
        
        Args:
            course_id: The course ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The updated course
        """
        course_id = self._get_item_id(course_id)
        
        return self.client.put(f'courses/{course_id}', **kwargs)
    
    def delete(self, course_id, **kwargs):
        """Delete a course.
        
        Args:
            course_id: The course ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The deleted course
        """
        course_id = self._get_item_id(course_id)
        
        return self.client.delete(f'courses/{course_id}', **kwargs)
    
    def list_students(self, course_id, **kwargs):
        """List students in a course.
        
        Args:
            course_id: The course ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: List of students
        """
        course_id = self._get_item_id(course_id)
        
        params = kwargs.get('params', {})
        params['enrollment_type'] = 'student'
        kwargs['params'] = params
        
        return list(self.client.paginate(f'courses/{course_id}/users', **kwargs))
    
    def list_assignments(self, course_id, **kwargs):
        """List assignments in a course.
        
        Args:
            course_id: The course ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: List of assignments
        """
        course_id = self._get_item_id(course_id)
        
        return list(self.client.paginate(f'courses/{course_id}/assignments', **kwargs))
    
    def list_modules(self, course_id, **kwargs):
        """List modules in a course.
        
        Args:
            course_id: The course ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: List of modules
        """
        course_id = self._get_item_id(course_id)
        
        return list(self.client.paginate(f'courses/{course_id}/modules', **kwargs)) 