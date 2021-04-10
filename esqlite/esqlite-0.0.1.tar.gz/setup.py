from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="esqlite",
    version="0.0.1",
    keywords=["pip", "esqlite"],
    description="esqlite means 'easy sqlite', is a sqlite3 wrapper.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT Licence",

    url="https://gitee.com/lixkhao/esqlite",
    author="Li Xiangkui",
    author_email="1749498702@qq.com",
    py_modules=['esqlite'],
    # packages=find_packages(),
    # include_package_data=True,
    platforms="any",
    install_requires=[]
)
