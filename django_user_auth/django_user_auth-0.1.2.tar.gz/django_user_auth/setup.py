from setuptools import setup, find_packages  

# with open("tencent_message\README.md", "r",encoding="utf-8") as fh:
#     long_description = fh.read()
long_description="""
0.1.1根据django rest framework的框架的status，优化异常时返回的结构\n
0.1.2 增加message截断功能增加安全性
"""
setup(  
    name = 'django_restful_response',  
    version = '0.1.2',
    # keywords = ('chinesename',),  
    description = 'django rest_framework 框架返回的Respone的异常不符合规范、增加error和message的描述',  
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = 'MIT tencent_message',  
    install_requires = ["django","djangorestframework"],  
    packages = ['django_restful_response'],  # 要打包的项目文件夹
    include_package_data=True,   # 自动打包文件夹内所有数据
    author = 'evanyang',  
    author_email = 'lightyiyi@qq.com',
    url = 'https://www.cnblogs.com/Evan-fanfan/',
    # packages = find_packages(include=("*"),),  
)  


# python setup.py check #检查写的有没有问题，有问题就直接报错了
# python setup.py sdist upload #压缩、并打包上传到pip源上，会在当前目录下产生一个dist文件夹
# #里面就是打好的压缩包
 
# python setup.py sdist #只压缩不上传，就是打成tar.gz这种安装包，给别人用的话直接给他安装包就可以了