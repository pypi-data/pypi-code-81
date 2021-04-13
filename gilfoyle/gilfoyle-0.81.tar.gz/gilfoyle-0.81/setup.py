from setuptools import setup
from setuptools import find_namespace_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gilfoyle',
    packages=find_namespace_packages(include=['gilfoyle.*']),
    version='0.81',
    license='MIT',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matt Clarke',
    author_email='matt@practicaldatascience.co.uk',
    url='https://github.com/practical-data-science/gilfoyle',
    download_url='https://github.com/practical-data-science/gilfoyle/archive/master.zip',
    keywords=['ecommerce', 'marketing', 'python', 'pandas', 'reports'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['pandas',
                      'seaborn',
                      'matplotlib',
                      'weasyprint',
                      'jinja2']
)
