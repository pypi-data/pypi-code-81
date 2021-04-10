import os
import re
import sys
import time

#发布版本
def publish():
    bg=time.time()
    if __name__=='__main__':
        path=os.path.dirname(os.path.dirname(__file__))

    else:
        path=sys.argv[0]

    with open(path+"\\setup.py",'r',encoding='utf8') as f:
        content=f.read()
        ver=re.findall('''version="([0-9]*).([0-9]*).([0-9]*)"''',content)
        arr=ver[0]
        arr=[int(arr[0]),int(arr[1]),int(arr[2])+1]
        content=re.sub("""version="[0-9]*.[0-9]*.([0-9]*)".*,""","""version="%d.%d.%d", """%(arr[0],arr[1],arr[2]),content)
    with open(path+"\\setup.py",'w',encoding='utf8') as f:
        f.write(content)

    os.chdir(path)
    cmd="python  setup.py sdist &  twine upload dist/* & rd /s /q dist & rd /s /q chtools.egg-info & python -m pip install chtools==%d.%d.%d"%(arr[0],arr[1],arr[2])
    pkg="zltask==%d.%d.%d"%(arr[0],arr[1],arr[2])
    os.system(cmd)

    ed=time.time()
    cost=int(ed-bg)
    print("cost %d s"%cost)


if __name__ == '__main__':

    publish()