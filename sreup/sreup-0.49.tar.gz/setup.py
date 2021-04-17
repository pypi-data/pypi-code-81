import setuptools

setuptools.setup(
    name='sreup',
    version='0.49',
    author="hoa",
    author_email="getmoneykhmt3@gmail.com",
    description="A Des of sreup",
    long_description="sreup",
    long_description_content_type="text/markdown",
    url="https://github.com/vtandroid/sreup",
    packages=setuptools.find_packages(),
    py_modules=['sreup'],
    install_requires=[
        'selenium','requests','gbak'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )