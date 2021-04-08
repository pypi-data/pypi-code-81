import codecs
import setuptools

def long_description():
    try:
        return codecs.open('README.rst', 'r', 'utf-8').read()
    except OSError:
        return 'Long description error: Missing README.rst file'

setuptools.setup(
    name='env2cli',
    version="0.1.0",
    author="Aviv Abramovich",
    author_email="AvivAbramovich@gmail.com",
    description="Converts environment variables into cli arguments for easy maintainable docker entry point",
    long_description=long_description(),
    url="https://github.com/AvivAbramovich/Env2Cli",
    project_urls={
        "Bug Tracker": "https://github.com/AvivAbramovich/Env2Cli/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)