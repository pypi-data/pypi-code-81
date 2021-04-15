def cons(num,var):
    import os
    import sys
    import re
    PATH_WITH_NAME = sys.argv[0]
    with open(PATH_WITH_NAME, 'r') as f:
        content = f.read()
        pattern = var + " ="
        pattern2 = var + "="
        length = len(re.findall(pattern, content))
        length2 = len(re.findall(pattern2, content))
        if length == length2:
            raise Errors(var)
        elif length >=2 :
            raise Errors(var)
        elif length2 >=2 :
            raise Errors(var)
        else:
            return num

class Errors(Exception):
    def __init__(self, val, message = f"cannot assign a value to final variable"):
        self.val = val
        self.message = message
        super().__init__(self.message)

