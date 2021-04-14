from setuptools import setup, find_packages

setup(
    name="yjb-scraper",
    version='0.70',
    description='YJB Dev',
    author='yJb',
    author_email='officialkrythex@gmail.com',
    packages=find_packages(),
    url='https://github.com/yjb-alevo/python-fun',
    install_requires=[
        'tqdm',
        'requests',
        'beautifulsoup4',
    ],
    entry_points='''
        [console_scripts]
        yjb-scraper=vscoscrape:main
    ''',
    keywords='yjb',
)
