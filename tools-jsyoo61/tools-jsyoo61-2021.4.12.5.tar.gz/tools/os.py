import os

__all__ = \
['listdir']

def listdir(path, isdir=False, join=False):
    '''
    :func listdir:

    :param path:
    :param isdir:
    :param join:
    '''
    # TODO: add :param isfile:
    # assert isdir and isfile, 'only one of argument "isdir" and "isfile" can be True'

    dir_list = os.listdir(path)
    dir_list_joined = [os.path.join(path, dir) for dir in dir_list]

    if join:
        dir_list = dir_list_joined
    # else: pass

    if isdir:
        return [dir for dir, dir_joined in zip(dir_list, dir_list_joined) if os.path.isdir(dir_joined)]
    else:
        return dir_list


# if __name__ == '__main__':
#     listdir('torch', isdir=False, join=False)
#     listdir('torch', isdir=False, join=True)
#     listdir('torch', isdir=True, join=False)
#     listdir('torch', isdir=True, join=True)
