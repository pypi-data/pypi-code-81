# Use this command for deploy.
#   python3 setup.py sdist bdist_wheel
#   python3 -m twine upload --skip-existing dist/*

import io
from setuptools import find_packages, setup

setup(name='ifmap',
      version='1.0.21',
      description='Infra Manager',
      long_description="Please refer to the https://github.com/da-huin/ifmap",
      long_description_content_type="text/markdown",
      url='https://github.com/da-huin/ifmap',
      download_url= 'https://github.com/da-huin/ifmap/archive/master.zip',
      author='JunYeong Park',
      author_email='dahuin000@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['simple_utils', 'template_manager', 'paramiko', 'boto3'],
      classifiers=[
          'Programming Language :: Python :: 3',
    ]
)
