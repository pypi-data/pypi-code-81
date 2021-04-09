from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='dissert_helper_functions_ksu_peter',
    version='0.0.6',
    description='A small package with collection of useful functions for dissertation',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n',
    license='MIT',
    packages=find_packages(),
    author="Peter Gates",
    author_email="pgate89@gmail.com",
    url="https://github.com/pomkos",
)

install_requires = [
    'numpy',
    'scipy',
    'pytz',
    'sqlalchemy',
    'pandas',
    'matplotlib',
    'seaborn'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)