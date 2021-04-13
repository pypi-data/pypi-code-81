import setuptools


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_reqs = parse_requirements("./requirements.txt")

with open("README.md", "r") as fh:
    long_description = fh.read()

reqs = install_reqs
setuptools.setup(
    name="alectio_sdk",
    version="0.6.15",
    author="Alectio",
    author_email="admin@alectio.com",
    url='https://github.com/alectio/SDK',
    description="Integrate customer side ML application with the Alectio Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['alectio=alectio_sdk.cli.cmd:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
        'Topic :: System :: Monitoring'
    ],
    python_requires=">=3.6",
    install_requires=install_reqs,
    package_data={"": ["config.json"]},
    include_package_data=True,
)
