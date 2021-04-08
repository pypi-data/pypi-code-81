from setuptools import setup, find_packages

# Get the long description from the README file
with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mlploy',
    version='0.0.2',
    author='Michele Dallachiesa',
    author_email='michele.dallachiesa@mlploy.com',
    packages=find_packages(exclude=["tests"]),
    scripts=[],
    url='https://www.mlploy.com',
    license='MIT',
    description='Machine Learning Inference with SQL',
    long_description=long_description,
    python_requires=">=3.6",
    install_requires=[
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],
)
