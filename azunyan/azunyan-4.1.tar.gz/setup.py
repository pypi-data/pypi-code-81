import setuptools

with open('README.md', 'r', encoding='utf8') as f:
    long_description = f.read()

setuptools.setup(
    name="azunyan",
    version="4.1",
    author="Elypha",
    author_email="i@elypha.com",
    description="Some simple functions I packed for self usage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Elypha/azunyan",
    project_urls={
        "Bug Tracker": "https://github.com/Elypha/azunyan/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)

# upgrade
# python3 -m pip install --user --upgrade setuptools wheel twine

# pack source distrib & wheels
# python3 setup.py sdist bdist_wheel

# upload
# python3 -m twine upload dist/*

# clean (change to CMD shell)
# rm -r azunyan.egg-info build dist

# upgrade
# python3 -m pip install --upgrade azunyan -i https://pypi.org/simple/
