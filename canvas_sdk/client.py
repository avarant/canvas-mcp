# canvas_sdk/client.py
import os
import requests
from urllib.parse import urljoin
from dotenv import load_dotenv

from .exceptions import CanvasAPIError
from .resources import Courses, Users, Assignments, Modules, Files
from .graphql_client import CanvasGraphQLClient

class CanvasClient:
    """Client for interacting with the Canvas LMS API.
    
    This client handles authentication and provides access to various Canvas API endpoints.
    """
    
    def __init__(self, api_token=None, api_url=None):
        """Initialize a Canvas API client.
        
        Args:
            api_token (str, optional): Canvas API token. If not provided, will attempt to load from CANVAS_TOKEN env var.
            api_url (str, optional): Canvas instance URL. If not provided, will attempt to load from CANVAS_HOST env var.
        """
        # Load environment variables if token or URL not provided
        if api_token is None or api_url is None:
            load_dotenv()
        
        self.api_token = api_token or os.getenv('CANVAS_TOKEN')
        self.api_url = api_url or os.getenv('CANVAS_HOST')
        
        if not self.api_token:
            raise ValueError("Canvas API token required. Provide as parameter or set CANVAS_TOKEN environment variable.")
        
        if not self.api_url:
            raise ValueError("Canvas URL required. Provide as parameter or set CANVAS_HOST environment variable.")
        
        # Ensure API URL ends with a slash
        if not self.api_url.endswith('/'):
            self.api_url += '/'
            
        # Base headers for all requests
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Initialize GraphQL client
        self.graphql = CanvasGraphQLClient(self.api_token, self.api_url)
        
        # Initialize resources
        self.courses = Courses(self)
        self.users = Users(self)
        self.assignments = Assignments(self)
        self.modules = Modules(self)
        self.files = Files(self)

    def _request(self, method, endpoint, params=None, data=None, json_data=None, files=None):
        """Make a request to the Canvas API.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint (without the base URL)
            params (dict, optional): Query parameters
            data (dict, optional): Form data
            json_data (dict, optional): JSON data
            files (dict, optional): Files to upload
            
        Returns:
            dict or list: Parsed API response
            
        Raises:
            CanvasAPIError: If the API returns an error
        """
        url = urljoin(self.api_url, f'api/v1/{endpoint}')
        
        response = requests.request(
            method,
            url,
            params=params,
            data=data,
            json=json_data,
            files=files,
            headers=self.headers
        )
        
        try:
            response.raise_for_status()
            
            if response.content and response.content.strip():
                return response.json()
            return None
        except requests.exceptions.HTTPError as err:
            error_message = str(err)
            if response.content:
                try:
                    error_data = response.json()
                    if 'errors' in error_data:
                        error_message = error_data['errors']
                except:
                    error_message = response.content.decode('utf-8')
                    
            raise CanvasAPIError(
                status_code=response.status_code,
                message=error_message,
                response=response
            )
            
    def get(self, endpoint, **kwargs):
        """Send a GET request to the Canvas API.
        
        Args:
            endpoint (str): API endpoint
            **kwargs: Additional arguments to pass to _request
            
        Returns:
            dict or list: Parsed API response
        """
        return self._request('GET', endpoint, **kwargs)
        
    def post(self, endpoint, **kwargs):
        """Send a POST request to the Canvas API.
        
        Args:
            endpoint (str): API endpoint
            **kwargs: Additional arguments to pass to _request
            
        Returns:
            dict or list: Parsed API response
        """
        return self._request('POST', endpoint, **kwargs)
        
    def put(self, endpoint, **kwargs):
        """Send a PUT request to the Canvas API.
        
        Args:
            endpoint (str): API endpoint
            **kwargs: Additional arguments to pass to _request
            
        Returns:
            dict or list: Parsed API response
        """
        return self._request('PUT', endpoint, **kwargs)
        
    def delete(self, endpoint, **kwargs):
        """Send a DELETE request to the Canvas API.
        
        Args:
            endpoint (str): API endpoint
            **kwargs: Additional arguments to pass to _request
            
        Returns:
            dict or list: Parsed API response
        """
        return self._request('DELETE', endpoint, **kwargs)
        
    def paginate(self, endpoint, **kwargs):
        """Paginate through all results of a GET request.
        
        Canvas API uses Link headers for pagination. This method automatically
        follows those links to retrieve all pages of results.
        
        Args:
            endpoint (str): API endpoint
            **kwargs: Additional arguments to pass to get()
            
        Yields:
            dict: Each item in the paginated response
        """
        params = kwargs.get('params', {})
        
        # Set a reasonable per_page value if not specified
        if 'per_page' not in params:
            params['per_page'] = 100
            
        kwargs['params'] = params
        
        while endpoint:
            response = self.get(endpoint, **kwargs)
            
            # Check if response is a list of items
            if isinstance(response, list):
                for item in response:
                    yield item
                    
                # Get link headers for pagination
                links = {}
                if hasattr(response, 'links') and response.links:
                    links = response.links
                
                # If there are no more pages, break
                if 'next' not in links:
                    break
                    
                # Get the next page URL
                next_url = links['next']['url']
                
                # Extract the endpoint from the full URL
                endpoint = next_url.split('/api/v1/')[1]
            else:
                # If the response is not a list, just yield it once and stop
                yield response
                break 