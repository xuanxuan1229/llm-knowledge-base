from functools import wraps
import logging
from exceptions import LLMRetryExhausted
import time

logger = logging.getLogger(__name__)
def retry(max_retries=3,backoff=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1,max_retries+1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"{func.__name__}第 {attempt} 次调用失败: {e}")
                    if attempt == max_retries:
                        raise LLMRetryExhausted(f"{func.__name__}重试 {max_retries} 次后仍失败: {e}")
                    time.sleep(backoff**attempt)
        return wrapper
    return decorator


