__all__ = (
    'check_either',
)


def check_either(first, second):
    def check_good(arg):
        if type(arg) is not tuple:
            if arg:
                return True, True
            else:
                return False, False
        else:
            return all(arg), any(arg)

    fg_all, fg_any = check_good(first)
    sg_all, sg_any = check_good(second)
    if fg_all and not sg_any:
        return True
    if sg_all and not fg_any:
        return True
    return False
