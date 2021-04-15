from __future__ import print_function
from os.path import abspath, join, dirname
import random


__title__ = 'data dummy'
__version__ = '0.1'
__author__ = 'keselyoleren'
__license__ = 'MIT'


full_path = lambda filename: abspath(join(dirname(__file__), filename))

FILES = {
    'name': full_path('data.names'),
    'address': full_path('data.address'),
}

def name():
    with open(FILES['name']) as list_name:
        name = random.choice(list(list_name))
        return name.rstrip("\n").capitalize()

def username():
    get_name = name().split()
    username, *_ = get_name
    return username

def email():
    return '{}@gmail.com'.format(username())

def phone():
    x = str(random.randint(810,850))
    y = str(random.randint(1,888)).zfill(4)
    z = str(random.randint(1,999)).zfill(4)
    return '+62{}-{}-{}'.format(x,y,z)

def ipv4():
    w = str(random.randint(1,255))
    x = str(random.randint(1,255))
    y = str(random.randint(1,255))
    z = str(random.randint(1,255))
    return '{}.{}.{}.{}'.format(w,x,y,z)

def address():
    with open(FILES['address']) as list_address:
        address = random.choice(list(list_address))
        return address.rstrip("\n")
        

def main():
    for a in range(10):
        print(address())

if __name__=="__main__":
    main()