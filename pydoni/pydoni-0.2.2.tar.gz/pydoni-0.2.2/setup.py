from setuptools import setup, find_packages

setup(
    name='pydoni',
    version=open('version').read(),
    description='A Python module for custom-built tools and maintained by Andoni Sooklaris.',
    # long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    # long_description_content_type='text/markdown',
    author='Andoni Sooklaris',
    author_email='andoni.sooklaris@gmail.com',
    url='https://github.com/tsouchlarakis/pydoni',
    license=open('LICENSE').read(),
    install_requires=open('requirements.txt').read(),
    packages=find_packages('pydoni'),
    package_dir={'': 'pydoni'},
    include_package_data=True,
    test_suite='tests'
)
