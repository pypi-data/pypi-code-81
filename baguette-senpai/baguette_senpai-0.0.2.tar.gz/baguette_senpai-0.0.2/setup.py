import setuptools

with open("README.md","r") as bs:
    long_description = bs.read()

setuptools.setup(
    name='baguette_senpai',
    version='0.0.2',
    author='JunyiZHONG',
    author_email='jyzh@yahoo.com',
    url='https://jooeys.github.io',
    description=u'mange de la baguette quand tu as faim',
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'baguette=BaguetteSenpai:baguette',
            'senpai=BaguetteSenpai:senpai'
        ]
    }
)