from dict import Dict
from int import Int
from float import Float
from set import Set
from list import List
from ordered_set import Ordered_set

def test_int():
    x=Int()
    x['test_int']=10
    x+='test_int',1
    print(x['test_int'])

def test_float():
    x=Float()
    x['test_f']=10.1
    x+='test_f',1.1
    print(x['test_f'])

def test_set():
    x=Set()
    x['test_set1']={1,2,3}
    x['test_set2']={5,6,7}
    x>>('test_set2','test_set1',5)
    print(x['test_set1'])
    print(x['test_set2'])
    # print(x['test_set'])
    # print(x+('test_set','test_set'))

    # for i in x.ergodic('test_set') :
    #     print(type(i))
    #     print(i)
    # for i in x['test_set']:
    #     print(type(i))
def test_list():
    x=List()
    x['list1']=[1,2,3],3
    # x+=('list1',[5,6,7])
    # x.push_front('list1',[1,2,3])
    # x['list2']=[-1,-2,-3]
    # x>>('list1','list2')
    # for i in x.ergodic('list1',0):
    #     print(i)
    print(x['list1'])

def dict_test():
    x=Dict()
    x['dict1']={'1':1,'2':2,'3':3}
    # x['dict1','5']='5'
    # del x['dict1','5']
    # for i in x.ergodic('dict1'):
    #     print(i)
    print(x['dict1'])

# x=Redis()
# x.exists('name')
# dict_test()
x=Ordered_set()
x['test']=[{1:30},{2:20},{3:10}]
print(x['test',True])