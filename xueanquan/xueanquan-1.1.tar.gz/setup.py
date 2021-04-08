from setuptools import setup

setup(
    name='xueanquan',
    version='1.1',
    packages=['xueanquan'],
    url='https://houtar.coding.net/public/xueanquan/python/git/files',
    install_requires='requests',
    python_requires='>=3',
    license='GNU GENERAL PUBLIC LICENSE',
    author='Houtarchat',
    author_email='admin@houtarchat.ml',
    description='Do xueanquan courses automatically',
    entry_points={
        'console_scripts':[
            'xueanquan=xueanquan:main'
            ]
        }
    
)
