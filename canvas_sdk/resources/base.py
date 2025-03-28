# canvas_sdk/resources/base.py

class BaseResource:
    """Base class for Canvas API resources.
    
    This class provides common methods and attributes for all resources.
    """
    
    def __init__(self, client):
        """Initialize a resource.
        
        Args:
            client (CanvasClient): The Canvas client instance
        """
        self.client = client
    
    def _get_item_id(self, item):
        """Extract the ID from an item.
        
        Args:
            item: A Canvas resource object or ID
            
        Returns:
            str: The ID of the resource
        """
        if isinstance(item, dict) and 'id' in item:
            return str(item['id'])
        return str(item) 