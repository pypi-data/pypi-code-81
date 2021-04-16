from setuptools import setup
setup(
    name="aufschlager",
    version="1.0.0",
    url="https://github.com/jenca-adam/pylots/tree/master/pylots/aufschlager",
    author="Adam Jenca",
    author_email="jenca.a@gjh.sk",
    description="Very simple web framework",
    long_description="""
Aufschlager is very simple Web framework.
```python
import aufschlager
aufschlager.route('/helloworld/','Hello world')
aufschlager.run(8080)
```
This will output 'Hello world' on url /helloworld/"""

)
