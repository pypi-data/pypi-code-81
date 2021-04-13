import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name='guildreader',
    version='1.1.3',
    author='Redmoogle',
    author_email='dakotamew@gmail.com',
    description='DiscordPy Guild Data Management Module',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/redmoogle/jsonreader',
    packages=setuptools.find_packages(),
    install_requires=[
        'ujson'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.5'
)
