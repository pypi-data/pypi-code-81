from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
     name='PyVM',
     version='0.0.2',
     scripts=['PyVM'] ,
     author="D.Fathi",
     author_email="Dhiabi.Fathi@gmail.com",
     description=" Python for operation between vector and matrix",
     long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
     url='',
     license='MIT',
     classifiers=classifiers,
     keywords='PyVM',
     packages=find_packages(),
     install_requires=['']
)
