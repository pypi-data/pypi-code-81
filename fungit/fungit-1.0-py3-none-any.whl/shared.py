TREE = {}

BOXS = {}

FUNC_BOX = {}

TIP = 'Pulling...'


class GitType:
    STATE = 1
    STATUS = 1 << 1
    COMMIT = 1 << 2
    BRANCH = 1 << 3
    STASH = 1 << 4
    CONTENT = 1 << 5
    Tip = 1 << 6
    Input = 1 << 7


class GitActionStatus:
    NONE = 1
    PULLING = 1 << 1


if __name__ == '__main__':
    print(GitActionStatus.NONE, GitActionStatus.PULLING)
