from setuptools import setup, find_packages

setup(name='peewee_base_model',
      version='0.0.5',
      description='Base model for peewee',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='peewee',
      url='https://github.com/GhostNA/peewee-base-model',
      author='Specter NA',
      author_email='naspecter@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'peewee',
      ],
      include_package_data=True,
      zip_safe=False)
