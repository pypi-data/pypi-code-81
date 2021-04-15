import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Shreekanth B K",
    author_email="shreekanth.bk@datagrokr.com",
    name='sparkutility',
    license="MIT",
    description='For functionalities that are missing in Spark SQL.',
    version='v0.1',
    long_description=README,
    long_description_content_type = "text/markdown",
    url='https://github.com/Shreekanth-BK/spark_utility',
    packages=setuptools.find_packages(),
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)