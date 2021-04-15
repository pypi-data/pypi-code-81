from setuptools import setup, find_packages

setup(name='qywx_app_message',
      version='2.0.6',
      description='qywx_app_message',
      long_description = 'https://github.com/not-know/qywx_app_message',
      url='https://github.com/not-know/qywx_app_message',
      author='zhr',
      author_email='zhangran1033@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires =  ["requests"],
      requires = ["requests"]
      )