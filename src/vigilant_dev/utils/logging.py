import logging
from functools import wraps

# Configure logging for the module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_decorator(func):
    """
    A decorator that logs the entry and exit of the function or method,
    including the class name if applicable.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        # The __qualname__ includes the class name for methods
        qual_name = func.__qualname__
        
        # Check if the function is a method by comparing __name__ and __qualname__
        if qual_name != func_name:
            # Extract class name from __qualname__
            class_name = qual_name.split('.')[0]
            logging.info(f"Entering: {class_name}.{func_name}")
        else:
            logging.info(f"Entering: {func_name}")
        
        result = func(*args, **kwargs)
        
        if qual_name != func_name:
            logging.info(f"Exiting: {class_name}.{func_name}")
        else:
            logging.info(f"Exiting: {func_name}")
            
        return result
    return wrapper