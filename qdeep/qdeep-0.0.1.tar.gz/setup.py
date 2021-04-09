from typing import List
import setuptools

_VERSION = "0.0.1"

# Short description.
short_description = "Simple Deep Q Learning framework."

# Packages needed for QDeep to run.
# The compatible release operator (`~=`) is used to match any candidate version
# that is expected to be compatible with the specified version.
REQUIRED_PACKAGES = [
    "dm-acme ~= 0.2.0",
    "dm-reverb ~= 0.2.0",
    "dm-sonnet ~= 2.0.0",
    "gym ~= 0.18.0",
    "jax ~= 0.2.12",
    "jaxlib ~= 0.1.65",
    "tensorflow ~= 2.4.1",
    "tensorflow-probability ~= 0.12.1",
    "trfl ~= 1.1.0",
    "scikit-image ~= 0.18.1"
]

# Packages which are only needed for testing code.
TEST_PACKAGES = [

]  # type: List[str]

# Loading the "long description" from the projects README file.
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='qdeep',
    version=_VERSION,
    author="Gabriel Guedes Nogueira (Talendar)",
    author_email="gabriel.gnogueira@gmail.com",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Talendar/qdeep",
    download_url="https://github.com/Talendar/qdeep/releases",
    # Contained modules and scripts:
    packages=setuptools.find_packages(),
    install_requires=REQUIRED_PACKAGES,
    tests_require=REQUIRED_PACKAGES + TEST_PACKAGES,
    # PyPI package information:
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT License",
    python_requires=">=3.6",
    keywords="machine-learning reinforcement-learning deep-q-learning",
)