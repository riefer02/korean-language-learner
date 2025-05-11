import functools
import hashlib
import json
from flask import current_app
import time

# Simple in-memory cache
_cache = {}


def cache_result(expire_seconds=3600):
    """Cache function results based on arguments"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key based on function name and arguments
            key_parts = [func.__name__]
            for arg in args:
                key_parts.append(str(arg))
            for k, v in sorted(kwargs.items()):
                key_parts.append(f"{k}:{v}")

            cache_key = hashlib.md5(json.dumps(key_parts).encode()).hexdigest()

            # Check if result is in cache and not expired
            current_time = time.time()
            if cache_key in _cache:
                result, timestamp = _cache[cache_key]
                if current_time - timestamp < expire_seconds:
                    current_app.logger.debug(f"Cache hit for {func.__name__}")
                    return result

            # Call the function and cache the result
            result = func(*args, **kwargs)
            _cache[cache_key] = (result, current_time)

            # Clean up old entries (simple garbage collection)
            for k in list(_cache.keys()):
                if current_time - _cache[k][1] > expire_seconds:
                    del _cache[k]

            return result

        return wrapper

    return decorator
