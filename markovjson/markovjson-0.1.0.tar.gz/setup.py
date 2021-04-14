from setuptools import setup

setup(
    name='markovjson',
    version='0.1.0',
    packages=['markovjson'],
    url='https://github.com/OpenJarbas/markovjson',
    license='apache-2',
    author='jarbasAi',
    install_requires=["json_database", "nltk"],
    author_email='jarbasai@mailfence.com',
    description='json meets markov chains'
)
