from setuptools import setup
setup(
    name='translapi',
    packages=['translapi','translapi.speech'],
    version='1.0.4',
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
    install_requires=['httplib2','wavio','pydub','gtts','langdetect','vlc'])
