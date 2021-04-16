import itertools

case_list = ['username', 'password']
value_list = ['correct', 'uncorrect', 'teshufuhao', 'overlong']


def gen_case(item=case_list, value=value_list):
    for i in itertools.product(item, value):
        print('input'.join(i))

def test_print():
     print("welcome")

if __name__ == '__main__':
    test_print()
