from setuptools import setup, find_packages

setup(
    name="schoolInfo",
    version="1.0.1.2",
    url="https://github.com/sunrabbit123/school-info_python",
    author="sunrabbit123",
    author_email="qudwls185@naver.com",
    description="간단하게 Neis API를 이용해보세요!",
    packages=find_packages(exclude=["tests"]),
    long_description=open("README.md", encoding="UTF-8").read(),
    long_description_content_type="text/markdown",
    install_requires=["aiohttp", "asyncio", "pytz"],
    python_requires=">=3.6",
    zip_safe=False,
    classifiers=["License :: OSI Approved :: MIT License"],
)
