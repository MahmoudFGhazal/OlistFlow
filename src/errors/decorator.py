from functools import wraps

from .handler import handle_error


def capture_error(stage, table=None):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            try:
                return func(*args, **kwargs)

            except Exception as error:

                handle_error(
                    error,
                    stage,
                    table
                )

                raise

        return wrapper

    return decorator