import setuptools


setuptools.setup(
    name="cpp-enum-class-string-idl",
    version="0.0.4",
    license='MIT',
    author="oneofthezombies",
    author_email="hunhoekim@gmail.com",
    description="cpp enum class string idl.",
    long_description=open('README.md').read(),
    long_description_content_type = 'text/markdown',
    url="https://github.com/oneofthezombies/cpp-enum-class-string-idl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
          'pyyaml',
      ],
)
