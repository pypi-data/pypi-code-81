import pathlib

from setuptools import setup ,find_packages


VERSION = '0.0.8'
DESCRIPTION = 'Type To Write API that may help you easier to make a writing apps without making it from scratch'
HERE = pathlib.Path(__file__).parent
README =  (HERE/"README.md").read_text()

# Setting up
setup(
    name="typetowritescreen",
    license="MIT",
    version=VERSION,
    author="Greg(GREGORIUS WILLSON)",
    author_email="willson2016pos@gmail.com",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['kivy','kivymd','gingerit','pillow'],
    keywords=['python', 'writing', 'writing api', 'writing gui', 'kivygui','writing kivy'],
    include_package_data=True,
    url='https://github.com/will702/typetowritescreen',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
