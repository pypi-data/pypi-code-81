import setuptools

'''
pysak setup.py
'''
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysak",
    version="0.0.7",
    author="jaded",
    author_email="jaded@foxmail.com",
    description="pysak 是一个简单、强大、干净的python公共函数库。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1Gbps/pysak",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
