from distutils.core import setup

setup(
    name = "zcc_Math",             #对外我们模块的名字
    version = "1.1.0",             #版本号
    description = "这是第一个对外发布的模块，测试哦",       #描述
    author = "zcc",                #作者
    author_email = "15652586725@163.com",
    py_modules = ["zcc_Math.zcc_demo1","zcc_Math.zcc_demo2"]      #要发布的模块
)