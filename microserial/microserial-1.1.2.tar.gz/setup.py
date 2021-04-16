from setuptools import setup
setup(
    name='microserial',
    version='1.1.2',
    install_requires=['pyserial'],
    packages=['microserial'],
    description="python module for reading data from microbit serial port",
    long_description_content_type='text/markdown',
    long_description='''
MicroSerial is Python module for receiving data from BBC micro:bit serial port.
Simplest example:
```python
from microserial import Microbit
m=Microbit()
#Microbit is stream type:
for i in m:
	print(i)
```

Or, a bit more complex example, but does the same thing:
```python
from microserial import Microbit
m=Microbit()
while True:
	print(m.readline())
```

You can redirect Microbit to stdout 
```python
from microserial import Microbit
m=Microbit()
#replaces stdout
m.replace_stio()
#reads from it
a=input()
#return back to normal
m.rstio()
```''',
    author="Adam Jenca",
    author_email='jenca.a@gjh.sk',
    url="https://github.com/jenca-adam/microbit/tree/master/microserial/",
)
