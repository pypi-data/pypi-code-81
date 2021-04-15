# -*- coding: utf-8 -*-
import setuptools

# 依赖的第三方包，python自有包不需要填写
requires = ['qrcode', 'pillow']

setuptools.setup(name="extpy",
                 version="0.0.9",
                 author="ilamy",
                 author_email='xethan@qq.com',
                 install_requires=requires,
                 packages=setuptools.find_packages(),
                 description="自用基础扩展库",
                 long_description=open('readme.md', encoding='UTF-8').read(),
                 long_description_content_type="text/markdown",
                 url='https://vip.kingdee.com/people/zuiqingquan-2147424412')
