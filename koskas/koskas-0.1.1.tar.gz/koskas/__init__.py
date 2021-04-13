import requests
__version__ = "0.1.0"
__author__ = 'Yair Koskas'
def greet():
    print('Hello, i\'m koskas and this is my python package!')
def joke():
    r = requests.get('http://api.icndb.com/jokes/random')
    s = r.text.encode('utf-8').decode()
    print(s[s.find('joke')+8:s.rfind('.')])
