from setuptools import setup
setup(
    name='translapi',
    version='1.0.1',
    description='Google Translate API',
    author="Adam Jenca",
    author_email="jenca.a@gjh.sk",
    long_description_format='text/markdown',
    long_description='''
Google Translate API and Google TTS
```python
from translapi import translate
print(translate('en','haw','To be or not to be').result)
```
For Google TTS:
```python
from translapi import translate
print(translate('en','de','To be or not to be').say())
```)''',
    requirements=['httplib2','wavio','pydub','gttsx','langdetect','vlc'])
