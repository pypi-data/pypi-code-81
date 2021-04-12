def gt0(val: int) -> int:
    """Value must be grater than 0"""
    if val <= 0:
        raise ValueError("bal must be greater than 0.")
    return val
