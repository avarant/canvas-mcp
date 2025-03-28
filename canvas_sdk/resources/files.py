from .base import BaseResource

class Files(BaseResource):
    """Interface to the Canvas Files API."""
    
    def list_course_files(self, course_id, **kwargs):
        """List files in a course.
        
        Args:
            course_id: The course ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: List of files
        """
        course_id = self._get_item_id(course_id)
        
        return list(self.client.paginate(f'courses/{course_id}/files', **kwargs))
    
    def list_user_files(self, user_id='self', **kwargs):
        """List files for a user.
        
        Args:
            user_id: The user ID, defaults to 'self'
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: List of files
        """
        user_id = self._get_item_id(user_id)
        
        return list(self.client.paginate(f'users/{user_id}/files', **kwargs))
    
    def get(self, file_id, **kwargs):
        """Get a single file.
        
        Args:
            file_id: The file ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: File object
        """
        file_id = self._get_item_id(file_id)
        
        return self.client.get(f'files/{file_id}', **kwargs)
    
    def update(self, file_id, **kwargs):
        """Update a file.
        
        Args:
            file_id: The file ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The updated file
        """
        file_id = self._get_item_id(file_id)
        
        return self.client.put(f'files/{file_id}', **kwargs)
    
    def delete(self, file_id, **kwargs):
        """Delete a file.
        
        Args:
            file_id: The file ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The deleted file
        """
        file_id = self._get_item_id(file_id)
        
        return self.client.delete(f'files/{file_id}', **kwargs)
    
    def upload(self, parent_folder_id, name, content, content_type, **kwargs):
        """Upload a file.
        
        This is a multi-step process:
        1. Get the upload URL and parameters from Canvas
        2. Upload the file to the provided URL
        3. Finalize the upload by telling Canvas it's complete
        
        Args:
            parent_folder_id: The ID of the folder to upload to
            name (str): The name of the file
            content: The file content (bytes or file-like object)
            content_type (str): The MIME type of the file
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The uploaded file
        """
        parent_folder_id = self._get_item_id(parent_folder_id)
        
        # Step 1: Get upload URL and parameters
        json_data = {
            'name': name,
            'size': len(content) if isinstance(content, bytes) else None,
            'content_type': content_type,
            'parent_folder_id': parent_folder_id
        }
        
        # Remove None values
        json_data = {k: v for k, v in json_data.items() if v is not None}
        
        init_response = self.client.post('files', json_data=json_data, **kwargs)
        
        upload_url = init_response.get('upload_url')
        upload_params = init_response.get('upload_params', {})
        
        if not upload_url:
            raise ValueError("Failed to get upload URL from Canvas API")
        
        # Step 2: Upload the file
        files = {'file': (name, content, content_type)}
        
        # We need to make a direct request here, not through the client
        # because the upload URL is not a Canvas API endpoint
        import requests
        upload_response = requests.post(upload_url, data=upload_params, files=files)
        upload_response.raise_for_status()
        
        # Step 3: Return the completed file info
        return upload_response.json()
    
    def list_folders(self, course_id, **kwargs):
        """List folders in a course.
        
        Args:
            course_id: The course ID
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: List of folders
        """
        course_id = self._get_item_id(course_id)
        
        return list(self.client.paginate(f'courses/{course_id}/folders', **kwargs))
    
    def create_folder(self, name, parent_folder_id, **kwargs):
        """Create a new folder.
        
        Args:
            name (str): The name of the folder
            parent_folder_id: The ID of the parent folder
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The created folder
        """
        parent_folder_id = self._get_item_id(parent_folder_id)
        
        json_data = kwargs.get('json_data', {})
        json_data['name'] = name
        json_data['parent_folder_id'] = parent_folder_id
            
        kwargs['json_data'] = json_data
        
        return self.client.post('folders', **kwargs) 