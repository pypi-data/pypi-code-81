from setuptools import setup, find_packages

setup(
    name = "testindatadev",
    version = "0.0.4",
    keywords = ["云测", "数据集","yuncedata", "testin", "testindatadev"],
    description = "数据集管理平台pythonSDK",
    long_description = "数据集管理平台pythonSDK，用于管理数据集",
    license = "MIT Licence",

    url = "http://ai.testin.cn/",
    author = "hide-in-code",
    author_email = "hejinlong@testin.cn",

    packages = find_packages(),
    entry_points={
          'console_scripts': [
              'tdav = testindatadev.cli.run:main'
          ]
      },
    include_package_data = True,
    platforms = "any",
    install_requires = [
        "click",
        "minio",
    ]
)
