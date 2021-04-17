#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Zhen Chen(chenzhen-win2009@163.com)
# Description: iLearnPlus: a comprehensive and automated machine-learning platform for nucleic acid and protein sequence analysis, prediction and visualization

from setuptools import setup, find_packages

setup(
    name = 'ilearnplus',
    version = '1.2',
    keywords='ilearnplus',
    description = 'A comprehensive and automated machine-learning platform for nucleic acid and protein sequence analysis, prediction and visualization',
    license = 'MIT License',
    url = 'https://github.com/Superzchen/iLearnPlus',
    author = 'SuperZhen',
    author_email = 'chenzhen-win2009@163.com',    
    packages=find_packages("src"),
    package_dir = {'':'src'},
    
    package_data = {
        # 任何包中含有.txt文件，都包含它
        '': ['*.txt'],
        # 包含demo包data文件夹中的 *.dat文件
        'ilearnplus': ['data/*.csv', 'data/*tsv', 'data/*txt', 'docs/*.pdf', 'images/*.*', 'models/*.pkl', 'util/data/*.txt',  'util/data/*.data'],
    },
    platforms = 'any',
    install_requires = [
        # 'PyQt5',
        'qdarkstyle',
        'numpy>=1.18.5',
        'pandas>=1.0.5',
        'sip',
        'datetime',
        'scikit-learn>=0.23.1',
        'scipy>=1.5.0',
        'lightgbm',
        'xgboost',
        'matplotlib>=3.1.1',
        'seaborn',
        'joblib',
        # 'multiprocessing',
        ],     
)