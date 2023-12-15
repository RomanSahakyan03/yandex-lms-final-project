class UrlError(Exception):
    """
    Custom exception class for handling invalid URL errors.

    Attributes:
        url (str): The invalid URL that caused the exception.
        message (str): A custom error message indicating the reason for the exception.

    Methods:
        __init__(self, url, message="Invalid URL"):
            Initializes the UrlError instance with the provided URL and an optional custom error message.

        __str__(self):
            Returns a string representation of the exception, including the error message and the invalid URL.

    Example:
        >>> raise UrlError("http://example.com", "Invalid protocol")
        UrlError: Invalid protocol - http://example.com
    """
    def __init__(self, url, message="Invalid URL"):
        self.url = url
        self.message = message
        super().__init__(message)
    
    def __str__(self):
        return f"UrlError: {self.message} - {self.url}"
