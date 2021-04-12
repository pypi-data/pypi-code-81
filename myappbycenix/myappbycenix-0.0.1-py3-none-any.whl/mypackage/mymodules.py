import pandas as pd
import numpy as np
from mypackage.submodel import subm1,subm2
a=5
b=2
"""
Source distribution源码包
$ python setup.py sdist --formats=gztar,zip
#当前目录会有dist（myapp-0.0.1.tar.gz，myapp-0.0.1.zip） 和 *.egg-info 目录


Format	Description	Notes
zip	zip file (.zip)	Windows 默认
gztar	gzip’ed tar file (.tar.gz)	Unix 默认
bztar	bzip2’ed tar file (.tar.bz2)	
xztar	xz’ed tar file (.tar.xz)	
ztar	compressed tar file (.tar.Z)	
tar	tar file (.tar)	
"""


"""
Built distribution
 python setup.py bdist --formats=rpm
 python setup.py bdist_rpm
 python setup.py bdist_wininst#增加build目录，不知道是什么
 #安装包
 Format	Description	Notes
gztar	gzipped tar file (.tar.gz)	Unix 默认
bztar	bzipped tar file (.tar.bz2)	
xztar	xzipped tar file (.tar.xz)	
ztar	compressed tar file (.tar.Z)	
tar	tar file (.tar)	
zip	zip file (.zip)	Windows 默认
rpm	RPM	
pkgtool	Solaris pkgtool	
sdux	HP-UX swinstall	
wininst	self-extracting ZIP file for Windows	
msi	Microsoft Installer.	
"""


"""
python setup.py bdist_wheel
执行成功后，目录下除了 dist 和 *.egg-info 目录外，还有一个 build 目录用于存储打包中间数据。

wheel 包的名称如 myapp-0.0.1-py3-none-any.whl
添加--universal参数可以myapp-0.0.1-py2.py3-none-any.whl
"""
def sumqp1(a,b):
    return subm1.sumquare(a,b)+1

def get_info():
    return subm2.info
if __name__ == '__main__':
    print(sumqp1(a,b))
    print(get_info())
