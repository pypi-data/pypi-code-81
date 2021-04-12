#这个地方相对目录引用只能这样用，在main里面会出错
#with open('./ssubmodel/useful.txt','r') as f:
try:
    with open('./submodel/ssubmodel/useful.txt','r') as f:
        info=f.readline()
except:info='cant read txt'

if __name__ == '__main__':
    print('info',info)