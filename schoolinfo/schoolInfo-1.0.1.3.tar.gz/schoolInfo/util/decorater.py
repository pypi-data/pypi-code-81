from functools import wraps

def except_keyError(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            raise KeyError("잘못된 인자값 또는 값이 없습니다.")

    return wrapper
