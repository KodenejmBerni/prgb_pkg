from typing import Callable


def if_window_still_requested(func: Callable):
    def wrapper(obj):
        if not obj.no_window_request.is_set():
            return func(obj)

    return wrapper
