#TODO: Check command
import os
# import pytest

def test_command():
    assert os.system('python -c "import code2doc"') == 0
    # assert True

p = 1_00_000
r = .10
n = 10
print(p*(1+r*n))
print(p*((1+r/12)**(n*12))*((1+r/12)**(n*12-1)-1))
# for n in range(1, 11):
#     ci = p*(1+r)**(n*12)
#     si = p*(1+r*n*12)
#     print(f'{n:2} {ci:10.2f} {si:10.2f}')

# i = p*(1.09)**2
# print(i)
# p = 1_00_000
# r = 0.09/12
# n = 24
# i = p*r*((1+r)**n)/((1+r)**n-1)
# print(i)
