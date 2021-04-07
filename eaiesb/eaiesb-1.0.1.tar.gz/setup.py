from setuptools import setup

setup(name='eaiesb',
      version='1.0.1',
      description='CSV Ingest-Transform-Persist',
      author='Akhil',
      author_email='akhil.kumar@eaiesb.com',
      url='https://www.eaiesb.com',
      packages=['eaiesb'],
      install_requires=['pyspark']
     )