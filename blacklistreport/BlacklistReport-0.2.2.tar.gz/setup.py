import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="BlacklistReport",
    version="0.2.2",
    author="dzellmer",
    description="Bad Reputation (Blacklisted IP) Incident Reporting.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://git.vcjames.io/soc/dailyblacklistreporting",
    packages=setuptools.find_packages(),
    install_requires=required,
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
