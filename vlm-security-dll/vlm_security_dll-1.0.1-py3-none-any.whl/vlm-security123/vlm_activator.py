import os,hashlib,re
from pathlib import Path
from ctypes import *
import ctypes


class VLM_security:
    _dll = None

    def __init__(self, dll_path ,soft_code):
        self._dll_path = dll_path
        self._dll = ctypes.windll.LoadLibrary(dll_path)
        self.soft_code = soft_code

    def get_code(self):
        GetCode = self._dll.GetCode
        GetCode.restype = c_char_p
        encode_bytes = GetCode().decode('utf-8')
        return encode_bytes

    def get_ver(self) -> str:
        '''
        Get VLM-Version
        :return: VLM-Version
        '''
        get_ver = self._dll.GetVer
        get_ver.restype = c_char_p
        value = get_ver()
        return value

    def init(self):
        result = self._dll["Initialize"](ctypes.c_char_p(self.soft_code.encode('utf-8')))
        return result >= 0

    def user_auth(self, account, pwd):
        result = self._dll["UserAuth"](ctypes.c_char_p(account.encode('utf-8')), ctypes.c_char_p(pwd.encode('utf-8')))
        return result

    def auth(self, auth_code):
        auth_res = self._dll["Auth"](ctypes.c_char_p(auth_code.encode('utf-8')))
        self.auth_code = auth_code
        return auth_res

    def auth_trial(self):
        return self.auth(self.soft_code)

    def encrypt(self, type, encode_bytes, key):
        encrypt = self._dll.Encrypt
        encrypt.restype = c_char_p
        result = encrypt(type, ctypes.c_char_p(encode_bytes.encode('utf-8')), ctypes.c_char_p(key.encode('utf-8'))).decode('utf-8')
        return result

    def decrypt(self, type, encode_bytes, key):
        decrypt = self._dll.Decrypt
        decrypt.restype = c_char_p
        result = decrypt(type, ctypes.c_char_p(encode_bytes.encode('utf-8')), ctypes.c_char_p(key.encode('utf-8'))).decode('utf-8')
        return result

    def get_validity(self):
        get_validity = self._dll.GetValidity
        get_validity.restype = c_char_p
        get_validity_str = get_validity().decode('utf-8')
        return get_validity_str

    def update(self, cmd=""):
        return self._dll.Update(cmd)

    def change_password(self, old_password, new_password):
        result = self._dll["ChangePassword"](ctypes.c_char_p(old_password.encode('utf-8')), ctypes.c_char_p(new_password.encode('utf-8')))
        return result == 0

    def get_user_type(self):
        user_type = self._dll["GetUserType"]()
        return user_type

    def user_register(self, account: str, pwd:str, type: bytes, bind: bytes, multi: bytes, point: int):
        account = ctypes.c_char_p(account.encode('utf-8'))
        pwd = ctypes.c_char_p(pwd.encode('utf-8'))
        result = self._dll["UserRegister"](account,pwd, type, bind, multi, point)
        return result

    def add_time(self,card:string,buyer:string,super:string,days:int,point:int):
        card = ctypes.c_char_p(card.encode('utf-8'))
        buyer = ctypes.c_char_p(buyer.encode('utf-8'))
        super = ctypes.c_char_p(super.encode('utf-8'))
        result = self._dll["AddTime"](card,buyer, super, days, point)
        return result

    def unbind(self):
        result = self._dll.Unbind()
        return result == 0

    def check_correct(self):
        GetCode = self._dll.GetCode
        GetCode.restype = c_char_p
        encode_bytes = GetCode()
        Decrypt = self._dll.Decrypt
        Decrypt.restype = c_char_p
        encode = str(self._dll.Decrypt(0, ctypes.c_char_p(encode_bytes), ctypes.c_char_p("456".encode('utf-8'))), encoding="utf-8")
        encode = str(self._dll.Decrypt(0, ctypes.c_char_p(encode.encode('utf-8')), ctypes.c_char_p("123".encode('utf-8'))), encoding="utf-8")
        return self.auth_code == encode

    def release(self):
        self._dll.Release()

    def is_valid(self):
        return self._dll.IsValid()

    def deduct_hour(self, hours: int):
        return self._dll.DeductHour(hours)

    def deduct_point(self, point: int):
        return self._dll.DeductPoint(point)

    def leave_msg(self, type, msg):
        self._dll.LeaveMsg(type, ctypes.c_char_p(msg.encode('utf-8')))

if __name__ == '__main__':
    Vbox = VLM_security(r"C:\Windows\VAuth.dll", "C06B11AD-D132-4C46-AF01-69A865BA43DE")

    result = Vbox.init()
    if not result:
        exit()
    return_value=Vbox.get_ver()

    result = Vbox.auth('01264D02-F472-423B-8E1D-6C218DB4C4FF')
    return_value=Vbox.add_time()
    Vbox.user_register("testvlm", 'bbb123456',0 ,0,1,1000)
    return_value=Vbox.user_auth("test123","test456")
    Vbox.change_password("test456","test789")
    return_value=Vbox.get_user_type()
    return_value=Vbox.get_validity()
    Vbox.update()
    return_value = Vbox.is_valid()
    return_value=Vbox.unbind()
    return_value=Vbox.deduct_point(10)
    return_value=Vbox.deduct_hour(5)

    Vbox.check_correct()
    Vbox.leave_msg(0, "123123123")
    t = Vbox.decrypt(0, Vbox.get_code(),"123")
    Vbox.release()
    exit()



