import pathlib
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent

README = (here / 'README.md').read_text()

setup(
    name = 'PygFW',
    author = 'Shaun Cameron',
    author_email = 'shauncameron13034@gmail.com',
    version= '0a',
    description = 'Create a simple yet effective server with and connect to it with a simple client!',
    long_description = README,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/shauncameron/PygFW',
    license = 'MIT',
    packages = find_packages(),
    install_requires = [
        'pygame'
    ]
)

print(' Packages Loaded >>', find_packages())