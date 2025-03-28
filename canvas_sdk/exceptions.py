# canvas_sdk/exceptions.py

class CanvasAPIError(Exception):
    """Exception raised for Canvas API errors.
    
    Attributes:
        status_code (int): HTTP status code returned by the API
        message (str): Error message
        response (requests.Response): Raw response object
    """
    
    def __init__(self, status_code, message, response=None):
        """Initialize the exception.
        
        Args:
            status_code (int): HTTP status code
            message (str or dict): Error message or dict of errors
            response (requests.Response, optional): Raw response object
        """
        self.status_code = status_code
        self.message = message
        self.response = response
        
        super().__init__(f"Canvas API Error ({status_code}): {message}")

class CanvasAuthError(CanvasAPIError):
    """Exception raised for authentication errors."""
    pass 