from setuptools import find_packages, setup
from os.path import join

from hytest.product import version

CLASSIFIERS = """
Development Status :: 4 - Beta
Intended Audience :: Developers
Topic :: Software Development :: Testing
License :: OSI Approved :: Apache Software License
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
""".strip().splitlines()

with open('README.md', encoding='utf8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name         = 'hytest',
    version      = version,
    author       = 'Patrik Jiang - Jiangchunyang',
    author_email = 'jcyrss@gmail.com',
    url          = 'http://www.python3.vip',
    download_url = 'https://pypi.python.org/pypi/hytest',
    license      = 'Apache License 2.0',
    description  = '一款系统测试自动化框架 Generic automation framework for QA testing',
    long_description = LONG_DESCRIPTION,
    keywords     = 'hytest automation testautomation',
    classifiers  = CLASSIFIERS,
    
    # https://docs.python.org/3/distutils/setupscript.html#listing-whole-packages  
    #   find_packages() 会从setup.py 所在的目录下面寻找所有 认为有效的python  package目录
    #   然后拷贝加入所有相关的 python 模块文件，但是不包括其他类型的文件
    packages     = find_packages(),
    
    # https://docs.python.org/3/distutils/setupscript.html#installing-package-data
    #  其他类型的文件， 必须在 package_data 里面指定 package目录 和文件类型
    package_data = {'hytest/utils': ['*.css','*.js']},
    
    include_package_data=True,
    
    install_requires=[   
          'rich',
          'dominate',
      ],
    entry_points = {
        'console_scripts': 
            [
                'hytest = hytest.run:run',
            ]
    }
)