

if __name__ == '__main__':


    from stack import Stack,StackException

    s = Stack()
    # 压栈测试
    for i in range(10):
        s.push(i)
    # 栈满测试
    try:
        s.push(1)
    except Exception as e:
        print(e)
    # 出栈测试
    for i in range(10):
        print(s.pop())
    # 栈空测试
    try:
        s.pop()
    except Exception as e:
        print(e)