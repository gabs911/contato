import logging

def log(func):
    logger = logging.getLogger('root')
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.debug(f"{func.__name__} ran with args: {args} and kwargs: {kwargs}, returned {result}")
        return result
    
    return wrapper

def logException(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger('root')
            logger.critical(f"Errored {func.__name__} with args: {args} and kwargs: {kwargs}")
            logger.exception(e)
            raise e
    return wrapper
            
