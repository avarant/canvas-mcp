from .base import BaseResource

class Modules(BaseResource):
    """Interface to the Canvas Modules API."""
    
    def list(self, course_id, include=None, **kwargs):
        """List modules in a course.
        
        Args:
            course_id: The course ID
            include (list, optional): Additional information to include
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: List of modules
        """
        course_id = self._get_item_id(course_id)
        
        params = kwargs.get('params', {})
        
        if include:
            params['include'] = include if isinstance(include, str) else ','.join(include)
            
        kwargs['params'] = params
        
        return list(self.client.paginate(f'courses/{course_id}/modules', **kwargs))
    
    def get(self, course_id, module_id, include=None, **kwargs):
        """Get a single module.
        
        Args:
            course_id: The course ID
            module_id: The module ID
            include (list, optional): Additional information to include
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: Module object
        """
        course_id = self._get_item_id(course_id)
        module_id = self._get_item_id(module_id)
        
        params = kwargs.get('params', {})
        
        if include:
            params['include'] = include if isinstance(include, str) else ','.join(include)
            
        kwargs['params'] = params
        
        return self.client.get(f'courses/{course_id}/modules/{module_id}', **kwargs)
    
    def create(self, course_id, name, **kwargs):
        """Create a new module.
        
        Args:
            course_id: The course ID
            name (str): The name of the module
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The created module
        """
        course_id = self._get_item_id(course_id)
        
        json_data = kwargs.get('json_data', {})
        json_data['module[name]'] = name
            
        kwargs['json_data'] = json_data
        
        return self.client.post(f'courses/{course_id}/modules', **kwargs)
    
    def update(self, course_id, module_id, **kwargs):
        """Update a module.
        
        Args:
            course_id: The course ID
            module_id: The module ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The updated module
        """
        course_id = self._get_item_id(course_id)
        module_id = self._get_item_id(module_id)
        
        return self.client.put(f'courses/{course_id}/modules/{module_id}', **kwargs)
    
    def delete(self, course_id, module_id, **kwargs):
        """Delete a module.
        
        Args:
            course_id: The course ID
            module_id: The module ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The deleted module
        """
        course_id = self._get_item_id(course_id)
        module_id = self._get_item_id(module_id)
        
        return self.client.delete(f'courses/{course_id}/modules/{module_id}', **kwargs)
    
    def list_items(self, course_id, module_id, **kwargs):
        """List items in a module.
        
        Args:
            course_id: The course ID
            module_id: The module ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: List of module items
        """
        course_id = self._get_item_id(course_id)
        module_id = self._get_item_id(module_id)
        
        return list(self.client.paginate(f'courses/{course_id}/modules/{module_id}/items', **kwargs))
    
    def get_item(self, course_id, module_id, item_id, **kwargs):
        """Get a single module item.
        
        Args:
            course_id: The course ID
            module_id: The module ID
            item_id: The item ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: Module item object
        """
        course_id = self._get_item_id(course_id)
        module_id = self._get_item_id(module_id)
        item_id = self._get_item_id(item_id)
        
        return self.client.get(f'courses/{course_id}/modules/{module_id}/items/{item_id}', **kwargs)
    
    def create_item(self, course_id, module_id, title, type, content_id, **kwargs):
        """Create a new module item.
        
        Args:
            course_id: The course ID
            module_id: The module ID
            title (str): The title of the item
            type (str): The type of item ('File', 'Page', 'Assignment', etc.)
            content_id: The ID of the content the item points to
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The created module item
        """
        course_id = self._get_item_id(course_id)
        module_id = self._get_item_id(module_id)
        content_id = self._get_item_id(content_id)
        
        json_data = kwargs.get('json_data', {})
        json_data['module_item[title]'] = title
        json_data['module_item[type]'] = type
        json_data['module_item[content_id]'] = content_id
            
        kwargs['json_data'] = json_data
        
        return self.client.post(f'courses/{course_id}/modules/{module_id}/items', **kwargs) 