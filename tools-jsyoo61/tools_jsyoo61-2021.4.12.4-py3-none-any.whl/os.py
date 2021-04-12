import os as _os

def listdir(path, isdir=True):
    if isdir:
        return [dir for dir in _os.listdir(path) if _os.path.isdir(_os.path.join(path, dir))]
    else:
        return _os.listdir(path)
