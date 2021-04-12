from setuptools import setup

setup(
    name="mdscript",
    version="0.1.3",
    packages=['mdscript', 'mdscript.transformers'],
    include_package_data=True,
    install_requires=["click", "watchdog"],
    url="https://github.com/Robinson04/mdscript",
    license="MIT",
    author="Inoft",
    author_email="robinson@inoft.com",
    description="Brings powerful scripting to markdown files with hot reload",
)
