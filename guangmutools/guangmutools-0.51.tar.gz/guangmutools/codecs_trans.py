# -*- encoding: utf-8 -*-
'''
@文件    :codecs_trans.py
@说明    :编码转换相关
@时间    :2021/02/23 10:38:58
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''

def Bytes2Str(b) -> str:
    '''
    确保参数是str类型
    '''
    if isinstance(b, bytes):
        return b.decode('utf-8')
    else:
        return str(b)

def Str2Bytes(s) -> bytes:
    if isinstance(s, str):
        return s.encode('utf-8')
    else:
        return None