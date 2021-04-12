from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools.command.install import install

with open("README.md", "r") as fh:
    long_description = fh.read()


def custom_command():
    import nltk
    nltk.download('averaged_perceptron_tagger')
    nltk.download("words")
    nltk.download('wordnet')


class Develop(develop):
    def run(self):
        develop.run(self)
        custom_command()


class EggInfo(egg_info):
    def run(self):
        egg_info.run(self)
        custom_command()


class Install(install):
    def run(self):
        # install.do_egg_install(self)  # to ensure packages in `install_requires` is installed
        install.run(self)
        custom_command()


setup(
    name='pyhumour',
    version='0.1.1',
    description='A module for the characterization and quantification of concise humour',
    license='BSD-3-Clause',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
    cmdclass={'install': Install,
              'develop': Develop,
              'egg_info': EggInfo},
    install_requires=[
        "pandas>=0.23.4",
        "scipy>=1.4.1",
        "numpy>=1.13.0",
        "wordfreq>=2.2.2",
        "hmmlearn>=0.2.3",
        "nltk>=3.3",
        "tensorflow>=2.2",
        "keras>=2.3.1",
        "requests>=2.25.1"
    ],
    extras_require={
        "dev": [
            "pytest>=5.4",
            "twine>=3.1",
            "nose>=1.3.7",
            "nose-timer>=1.0.1",
            "coverage>=5.5"
        ]
    },
    setup_requires=['nltk'],
    url="https://github.com/mellon-collie/pyhumour",
    author='The PyHumour Development Team',
    author_email='pyhumour-devs@googlegroups.com',
)
