from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyImageOp',
    packages=['PyImageOp'],
    version='0.1.022b',
    license='MIT',
    description='Small library to help in live editing image with python, for now beta version',
    author='allahaka',
    author_email='allahaka90@gmail.com',
    url='https://github.com/allahaka/PyImageOp',
    download_url='https://github.com/allahaka/PyImageOp/archive/refs/tags/0.1.01b.tar.gz',
    keywords=['Image', 'AI', 'ImageCapture', 'Image Filters', 'Image Recognition'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'scipy',
        'opencv_python',
        'numpy',
        'pillow',
        'mss',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
