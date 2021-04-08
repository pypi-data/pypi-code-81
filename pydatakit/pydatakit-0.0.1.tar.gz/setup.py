from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pydatakit',
  version='0.0.1',
  description='This library is for data science user',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Mutesasira Denis',
  author_email='Dencoding4@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='pydatakit', 
  packages=find_packages(),
  install_requires=['pandas', 'pandas_profiling', 'sklearn', 'plotly', 'sweetviz', 'matplotlib', 'xgboost', 'lightgbm', 'klib', 'keras','tensorflow'])

# create dist
# python setup.py sdist

# command for upload 
# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*