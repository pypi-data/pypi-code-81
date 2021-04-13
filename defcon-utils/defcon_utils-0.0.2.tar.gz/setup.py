from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Common utility functions and classes by DefCon-007'
LONG_DESCRIPTION = ''

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="defcon_utils", 
        version=VERSION,
        author="Ayush Goyal",
        author_email="ayushgoyal.iitkgp@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['requests', 'python-dateutil', 'pytz'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)