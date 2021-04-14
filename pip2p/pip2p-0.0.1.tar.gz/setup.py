import pathlib
from setuptools import setup


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='pip2p',
    version='0.0.1',
    description="install private packages which store in svn repository",
    author="ticktick",
    author_email="cyxia90s@163.com",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    # packages=["pip2p"],
    py_modules=['pip2p'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pipp=pip2p:pipp
    ''',
)
