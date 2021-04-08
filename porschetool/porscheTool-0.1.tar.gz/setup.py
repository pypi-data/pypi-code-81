from setuptools import setup, find_packages, Distribution


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


setup(name='porscheTool',
      version='0.1',
      author='xingbi',
      description='porscheTool',
      zip_safe=False,
      packages=find_packages(),
      include_package_data=True,
      distclass=BinaryDistribution)
