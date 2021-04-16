
from setuptools import setup, find_packages  

setup(  
    name = 'exDEG',  
    version = '1.0.0',
    # keywords = ('chinesename',),  
    description = 'A python library for screening classified dignosed Gene',  
    license = 'MIT License',  
    install_requires = ['Pyomic'],  
    packages = ['exDEG'],  # 要打包的项目文件夹
    include_package_data=True,   # 自动打包文件夹内所有数据
    author = 'ZehuaZeng',  
    author_email = 'Starlitnightly@163.com',
    url = 'https://github.com/Starlitnightly/exDEG',
    # packages = find_packages(include=("*"),),  
)  
