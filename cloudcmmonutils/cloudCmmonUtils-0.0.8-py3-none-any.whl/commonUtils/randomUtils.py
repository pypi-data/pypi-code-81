from builtins import print, int, str, range, len, AssertionError
import time
import random


def create_mobile_phone_number():
    '''
    创建虚拟手机号：193...
    :return:
    '''
    currentTime = int(time.time())*1000
    currentTime = str(currentTime)[2:10]
    phoneNum = '193'+currentTime
    print('phoneNum:%s'%phoneNum)
    return phoneNum

def create_random_int_by_len(length):
    '''
    创建指定长度的整型数
    :param len: 指定创建的随机正数长度
    :return: 返回创建的随机整数
    '''
    try:
        length = int(length)
    except:
        raise AssertionError("指定的随机数长度应是数字类型")

    intArr = '0123456789'
    randomInt = ''
    leng = len(intArr)
    if length < 1:
        return ''
    elif len == 1:
        index = random.randint(1,leng-1)
        randomInt = intArr[index]
    else:
        index = random.randint(1, leng - 1)
        randomInt = intArr[index]
        for i in range(length-1):
            randomInt += intArr[random.randint(1, leng - 1)]
    return randomInt

if __name__ == '__main__':
    print(create_random_int_by_len('1'))