import setuptools

with open("README.md",'r') as f:
	description_ = f.read()


setuptools.setup(
	name = "pfmcnninitialization", #模块名称
	version = "0.2", #版本号
	author = "zxzong", 
	author_email = '274573863@qq.com',
	description = "A module for constructing parameter initialization matrix of convolutional neural network for genomics using PFM matrix information of transcription factors in Jaspar database.",
    long_description = description_,
    long_description_content_type = 'text/markdown',
    url = '',
    packages = setuptools.find_packages(),#自动寻找项目中导入的模块

    #模块相关元信息（描述信息，说明开发语言、操作系统、版权）
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
    ],
     
    #需要自动安装的依赖 
    install_requires=[
    "numpy",
    "pandas",
    "random2"],
     
    python_requires=">=3.6"

	)