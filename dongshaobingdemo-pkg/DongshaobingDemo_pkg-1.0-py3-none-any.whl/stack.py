class StackException(Exception):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.data


class Stack(object):
    def __init__(self, size=10):
        self.S = []
        self.size = size  # 栈大小
        self.top = -1  # 栈顶位置

    def setSize(self, size):
        # 设置栈的大小
        self.size = size

    def isEmpty(self):
        # 判断栈是否为空
        if self.top == -1:
            return True
        else:
            return False

    def isFull(self):
        # 判断栈是否满
        if self.top == self.size - 1:
            return True
        else:
            return False

    def peek(self):
        # 查看栈顶的对象，但不移除
        if self.isEmpty():
            raise StackException('StackUnderflow')
        else:
            element = self.S[-1]
            return element

    def pop(self):
        # 移除栈顶对象，并返回该对象的值
        if self.isEmpty():
            raise StackException('StackUnderflow')
        else:
            element = self.S[-1]
            self.top = self.top - 1
            del self.S[-1]
            return element

    def push(self, element):
        # 把对象压入栈顶
        if self.isFull():
            raise StackException('StackOverflow')
        else:
            self.S.append(element)
            self.top = self.top + 1

