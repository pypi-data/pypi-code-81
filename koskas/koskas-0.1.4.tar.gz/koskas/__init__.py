import requests
__version__ = "0.1.4"
__author__ = 'Yair Koskas'
def greet():
    print('Hello, i\'m koskas and this is my python package!')
def joke():
    r = requests.get('http://api.icndb.com/jokes/random')
    s = r.text.encode('utf-8').decode()
    s = s.replace('&quot;','"')
    print(s[s.find('joke')+8:s.rfind('.')])
def isprime(n):
    for i in range(math.ceil(math.sqrt(n))):
        if n%i == 0:
            return False
    return False
