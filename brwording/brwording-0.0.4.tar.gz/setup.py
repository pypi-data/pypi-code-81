from setuptools import setup, find_packages
import pathlib
import pkg_resources

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(name='brwording',
version='0.0.4',
description='brwording - Processamento de Linguagem Natural em Português',
long_description=open('README.md').read(),
long_description_content_type='text/markdown',
url='https://github.com/dbranquinho/brwording',
author='Delermando Branquinho Filho',
author_email='delermando@gmail.com',
license='MIT',
packages=['brwording'],
include_package_data=True,
package_data={'':['config/*']},
install_requires=install_requires,
zip_safe=False)


