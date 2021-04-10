from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="edata",
    version="0.0.1",
    keywords=["pip", "edata"],
    description="edata means 'easy data', is a wrapper of csv, xlrd, xlwt, pylightxl",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT Licence",

    url="https://gitee.com/lixkhao/edata",
    author="Li Xiangkui",
    author_email="1749498702@qq.com",
    py_modules=['edata'],
    # packages=find_packages(),
    # include_package_data=True,
    platforms="any",
    install_requires=['pylightxl', 'xlrd', 'xlwt']
)
