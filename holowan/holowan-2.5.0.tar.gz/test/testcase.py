
def mytest(**kwargs):
    myDict = kwargs.keys()
    for m in myDict:
        print(m)

if __name__ == '__main__':
        mytest(cursor="haha")