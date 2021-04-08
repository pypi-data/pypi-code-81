import setuptools
setuptools.setup(name='holowan',
                 version='2.3.6',
                 packages=setuptools.find_packages(),
                 package_data={"holowan": ["resources/*.xml", "resources/*.ini"]}
                )
