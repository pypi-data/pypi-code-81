from setuptools import setup

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()

setup(name='lolzapi',
      version='0.3.0',
      description='',
      packages=['lolzapi'],
      long_description=long_description,
      long_description_content_type='text/markdown', 
      author_email='cotanton111@gmail.com',
      zip_safe=False)
