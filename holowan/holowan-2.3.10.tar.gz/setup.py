import setuptools
setuptools.setup(name='holowan',
                 version='2.3.10',
                 description='This is a API for HoloWAN',
                 author='Dee',
                 packages=setuptools.find_packages(include=['holowan', 'utils'], exclude=['test']),
                 package_data={"holowan": ["resources/*.xml", "resources/*.ini"]}
                )
