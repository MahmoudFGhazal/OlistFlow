from functools import wraps

from .handler import handle_error


def capture_error(stage, table=None):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            try:
                return func(*args, **kwargs)

            except Exception as error:
                if not getattr(error, "_already_logged", False):
                    handle_error(
                        error,
                        stage,
                        table
                    )
                    error._already_logged = True
                raise

        return wrapper

    return decorator