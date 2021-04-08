from os import path as os_path
import setuptools

this_directory = os_path.abspath(os_path.dirname(__file__))

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setuptools.setup(
    name="scu-api",
    version="0.0.1",
    author="CarOL",
    author_email="herixth@gmail.com",
    description="An api provide for Sichuan University",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/hx-w/scu-api",
    packages=setuptools.find_packages(),
    license="GNU General Public License v3.0",
    python_requires='>=3.6',
    install_requires=read_requirements('requirements.txt'),
)
