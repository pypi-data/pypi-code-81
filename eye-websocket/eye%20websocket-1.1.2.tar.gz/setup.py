from setuptools import setup

setup(
    name = 'eye websocket',
    version = '1.1.2',
    author = 'Arthur Bogiano',
    author_email = 'arthurprosel@gmail.com',
    packages = ['eye'],
    install_requires=['websockets', 'asyncio'],

    description = 'It is a utility to simplify service creation processes using websockets',

    long_description = 'pt-br: É um utilitário para simplificar processos de criação de serviços utilizando websockets',

    url = 'https://github.com/ArthurBogiano/eye',

    project_urls = {
        'Código fonte': 'https://github.com/ArthurBogiano/eye'
    },

    license = 'MIT',
    keywords = 'websockets websocket socket web server',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ]
)