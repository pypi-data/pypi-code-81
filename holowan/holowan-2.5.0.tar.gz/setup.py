import setuptools
setuptools.setup(name='holowan',
                 version='2.5.0',
                 description='This is a API for HoloWAN',
                 author='Dee',
                 packages=setuptools.find_packages(),
                 package_data={"holowan": ["resources/*.xml", "resources/*.ini"]}
                )
