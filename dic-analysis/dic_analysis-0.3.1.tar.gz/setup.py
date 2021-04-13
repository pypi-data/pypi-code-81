from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='dic_analysis',
    version='0.3.1',
    packages=find_packages(),
    license='MIT',
    author='Peter Crowther',
    author_email='',
    description='Functions for analysis of tensile DIC experiments',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
    ],
    install_requires=["pandas",
                      "numpy",
                      'tqdm',
                      'PyYAML'
                      ]
)
