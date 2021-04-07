# coding: utf-8
"""Setup script for IVA NN applications service."""

from setuptools import find_packages, setup

setup(name='iva_applications',
      version='9.0.1',
      author='IVA Technologies',
      author_email='engineering@iva-tech.ru',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      install_requires=[
            'matplotlib',
            'Pillow',
            'scikit-build',
            'opencv-python',
            'scipy==1.4.1',
            'scikit-image',
            'keras==2.2.4',
            'pydrive'
      ],
      extras_require={
            'tensorflow': ['tensorflow==2.4.1']
      })
