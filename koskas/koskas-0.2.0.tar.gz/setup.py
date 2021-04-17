from setuptools import setup

setup(
    name='koskas',
    version='0.2.0',    
    description='My python package',
    scripts=['joke'],
    url='https://github.com/yairKoskas/koskas',
    author='Yair Koskas',
    author_email='yairi2003@gmail.com',
    license='BSD 2-clause',
    packages=['koskas'],
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
