import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
        name="nlidatamanagement",
        version="0.0.3",
        author="Luis Sordo Vieira",
        author_email="luis.sordovieira@medicine.ufl.edu",
        description="A tkinter GUI for uploading tagged data to Girder and Zotero.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/NutritionalLungImmunity/data-management",
        project_urls={
            "Bug Tracker": "https://github.com/NutritionalLungImmunity/data-management/issues",
            },
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        python_requires='>=3.6',
        install_requires=[
            'flake8>=3.7.9',
            'pytest>=5.4.1',
            'girder-client>=3.1.0',
            'attrs>=19.3.0',
            'pyzotero>=1.4.16',
            'pandas>=1.0.5',
            'pillow>=8.0.1',
            'pytablewriter>=0.58.0',
            ],
        entry_points={
            'console_scripts': [
                'nlidatamanagement=nlidatamanagement.main:main',
                ],
            },
        include_package_data=True,
        )
