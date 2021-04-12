#这个地方相对目录引用只能这样用，在main里面会出错
#with open('./ssubmodel/useful.txt','r') as f:#./submodel/ssubmodel
import os
#没啥好办法感觉
BASE=os.path.dirname(os.path.abspath(__file__))
try:
    with open(BASE+'/ssubmodel/useful.txt','r') as f:
        info=f.readline()
except:
    info='icant'

if __name__ == '__main__':
    print(os.path.abspath(__file__))
    print('info',info)