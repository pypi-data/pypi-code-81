from setuptools import setup, find_packages

setup(
    name='Gask',
    version='0.1',
    packages=find_packages(),
    #package_dir={'': 'gask'},
    url='https://github.com/RyanVanDijck/Gask',
    license='GPLv3',
    author='ryan',
    author_email='rvandijck02@outlook.com',
    entry_points={
        'console_scripts': [
            'gask = gask.gask:main',
        ],
    },
    install_requires=['gitpython',
                      'terminaltables',
                      'termcolor',
                      'pick'],
    extras_require={
        'burndown': ['matplotlib'],
    },
    description='A git backed task management system'

)
