# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""


def _process_requirements():
    packages = open('requirements.txt').read().strip().split('\n')
    requires = []
    for pkg in packages:
        if pkg.startswith('git+ssh'):
            return_code = os.system('pip install {}'.format(pkg))
            assert return_code == 0, 'error, status_code is: {}, exit!'.format(return_code)
        else:
            requires.append(pkg)
    return requires


setup(
    name="httprunnerlt",
    version="0.0.5",
    description="this is fix assert",
    license="MIT",
    author="liutao",
    author_email="kongxuanr@163.com",
    url="http://www.example.com/~cschultz/bvote/",
    install_requires=_process_requirements(),
    packages=find_packages(),
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
    entry_point={'console_scripts': ["hrunlt = httprunnerlt.cli:main_hrun_alias",
                                     "har2caselt=httprunnerlt.cli:main_har2case_alias",
                                     "hmakelt=httprunnerlt.cli:main_make_alias",
                                     "httprunnerlt=httprunnerlt.cli:main",
                                     "locustslt=httprunnerlt.ext.locust:main_locusts"]}
    # 包搜集
    # package_dir={"":"src"},
    # py_modules=["single_module"],
    # package_data={"buddha":["*.txt"]},
    # data_files=[("Doc",["src/buddha_doc.txt"])],
    # scripts=["src/buddha.bat"],
    # twine upload --repository pypi dist/* --verbose
    # python setup.py sdist bdist bdist_wheel upload
    #pipreqs ./ --encoding=utf8 --force

)
