import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='planetary',
      version='0.13',
      description='Tools for doing planetary science in Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github/phayne',
      author='Paul O. Hayne',
      author_email='paul.hayne@colorado.edu',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
		'numpy',
		'matplotlib',
      ],
      zip_safe=False)
