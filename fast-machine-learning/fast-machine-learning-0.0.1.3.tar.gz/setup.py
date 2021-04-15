from setuptools import setup, find_packages

setup(
    name='fast-machine-learning',
    version='0.0.1.3',
    description=(
        'Enhance and remake my first pkg luktianutl (partially in current) which is still under remaking. '
    ),
    author='luktian',
    author_email='luktian@shu.edu.cn',
    maintainer='luktian',
    maintainer_email='luktian@shu.edu.cn',
    license='BSD License',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*", 
                                    "__pycache__", "fml001.pyproj", "fml001.pyproj.user"]),
    platforms=["windows"],
    python_requires=">=3.6",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'sklearn',
        'numpy',
        'scipy'
    ],
)