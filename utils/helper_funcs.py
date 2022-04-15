
import asyncio
from functools import wraps


def async_to_sync(func):
    @wraps(func)
    def sync_func(*args, **kwargs):
        loop = asyncio.get_event_loop()
        coroutine = func(*args, **kwargs)
        return loop.run_until_complete(coroutine)
    return sync_func
