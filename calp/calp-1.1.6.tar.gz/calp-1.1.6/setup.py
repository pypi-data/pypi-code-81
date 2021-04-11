from setuptools import setup, find_packages

VERSION = '1.1.6'
DESCRIPTION = 'A simple calculating package'
LONG_DESCRIPTION = 'Simply calculate large numbers without sperating'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="calp",
        version=VERSION,
        author="Tahir Murata",
        author_email="tahirmurata83@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'calculating', 'calculator'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)