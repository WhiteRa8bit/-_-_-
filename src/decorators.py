import functools
import datetime


def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            try:
                result = func(*args, **kwargs)
                end_time = datetime.datetime.now()
                log_message = f"{func.__name__} ok. Start time: {start_time}, End time: {end_time}\n"
                print(log_message)
            except Exception as e:
                end_time = datetime.datetime.now()
                log_message = (
                    f"{func.__name__} error: {str(e)}. "
                    f"Inputs: {args}, {kwargs}. Start time: {start_time}, End time: {end_time}\n"
                )
                print(log_message)
                result = None
                if filename is not None:
                    with open(filename, 'a') as f:
                        f.write(log_message)
                else:
                    print(log_message)
                return result

            if filename is not None:
                with open(filename, 'a') as f:
                    f.write(log_message)
            else:
                print(log_message)

            return result
        return wrapper
    return decorator
