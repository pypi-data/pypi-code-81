import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="qtfn",
    version="0.1",
    author="mellofn",
    description="fortnite lobbybot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'crayons',
        'dhooks',
        'os',
        'discord',
        'discord.py',
        'timeago',
        'jinja2',
        'jaconv',
        'requests',
        'psutil',
        'pypresence',
        'BenBotAsync',
        'uvloop',
        'sanic',
        'aiohttp'
    ],
)
