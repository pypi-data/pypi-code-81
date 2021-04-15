from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'GoogleDriveDown',
    version = '0.0.3',
    description = 'This module allows you to download all the content from a shared google drive url to specified directory.',
    long_description = long_description + '\n\n' + open('changelog.txt').read(),
    long_description_content_type = 'text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing :: Linguistic',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows :: Windows 10'],
    keywords = 'Google Google-Drive',
    url = '',
    author = 'Aditya Sisodiya',
    author_email = 'adityasisodiya2803@gmail.com',
    license = 'MIT',
    packages = find_packages(),
    install_requires = ['PyDrive==1.3.1', 'pandas==1.1.5'],
    include_package_data = True,
    zip_safe = False
)