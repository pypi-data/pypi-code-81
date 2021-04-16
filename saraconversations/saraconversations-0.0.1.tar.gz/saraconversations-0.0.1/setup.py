from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='saraconversations',
  version='0.0.1',
  description='conversations of sara',
  long_description=open('README.txt').read(),
  url='',  
  author='Pyrobit',
  author_email='pyrobit.technologies@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Saraconversations', 
  packages=find_packages(),
  install_requires=[''] 
)