from typing import Any, Callable


def deprecated(
    replacement: Callable[..., Any] | None = None,
) -> Callable[..., Any]:
    """
    Decorator to mark a function as deprecated (to be used in the parent module)

    :param replacement: The function that should be used instead of the
    deprecated function.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"warning: {func.__name__} is deprecated.")
            if replacement is not None:
                print(f"use {replacement} instead.")
            return func(*args, **kwargs)

        return wrapper

    return decorator
