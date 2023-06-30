import logging

def log(func):
    logger = logging.getLogger('root')
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.debug(f"{func.__name__} ran with args: {args} and kwargs: {kwargs}, returned {result}")
        return result
    
    return wrapper
