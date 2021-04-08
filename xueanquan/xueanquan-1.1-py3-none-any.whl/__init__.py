from xueanquan.method import do

version = '1.0'
author = 'Houtarchat'
author_email = 'admin@houtarchat.ml'
description = 'Complete xueanquan tasks automatically'


def main():
    do(input('Input your username:'), input('Input your password:'))

if __name__ == '__main__':
    main()
