# canvas_sdk/graphql_client.py
import requests
from urllib.parse import urljoin

from .exceptions import CanvasAPIError

class CanvasGraphQLClient:
    """Client for interacting with the Canvas LMS GraphQL API."""
    
    def __init__(self, api_token, api_url):
        """Initialize a Canvas GraphQL API client.
        
        Args:
            api_token (str): Canvas API token
            api_url (str): Canvas instance URL
        """
        self.api_token = api_token
        
        # Ensure API URL ends with a slash
        if not api_url.endswith('/'):
            api_url += '/'
            
        self.api_url = urljoin(api_url, 'api/graphql')
        
        # Headers for all requests
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
    def query(self, query, variables=None):
        """Execute a GraphQL query.
        
        Args:
            query (str): The GraphQL query
            variables (dict, optional): Variables for the query
            
        Returns:
            dict: The query result
            
        Raises:
            CanvasAPIError: If the API returns an error
        """
        payload = {
            'query': query,
            'variables': variables or {}
        }
        
        response = requests.post(
            self.api_url,
            json=payload,
            headers=self.headers
        )
        
        try:
            response.raise_for_status()
            result = response.json()
            
            if 'errors' in result:
                raise CanvasAPIError(
                    status_code=response.status_code,
                    message=result['errors'],
                    response=response
                )
                
            return result.get('data', {})
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