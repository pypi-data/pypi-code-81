def except_keyError(func):
    def wrapper():
        try:
            func()
        except KeyError:
            raise KeyError("잘못된 인자값 또는 값이 없습니다.")

    return wrapper
