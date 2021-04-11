import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sciscripts",
    version="3.0.4",
    author="T Malfatti",
    author_email="malfatti@disroot.org",
    description="Scripts for controlling devices/running experiments/analyzing data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/malfatti/SciScripts",
    packages=setuptools.find_packages(),
    install_requires=[
        'asdf', 'h5py', 'matplotlib', 'numpy', 'pandas', 'pyserial', 'rpy2', 'scipy', 'sounddevice'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=3.6',
)
