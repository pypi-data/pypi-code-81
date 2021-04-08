from pathlib import Path
from ctypes import *
import ctypes
import sys
import shutil


class VLM_security:
    _dll = None

    def __init__(self, dll_path, soft_code):
        self._dll_path = dll_path
        self._dll = ctypes.windll.LoadLibrary(dll_path)
        self.soft_code = soft_code
        self.check_vnc()

    def check_vnc(self):
        path = os.path.dirname(sys.executable)
        if not os.path.exists((os.path.join(path, 'VServerGroup.vnc'))):
            print('check *.vnc file')
            exit()

    def get_code(self):
        '''
        獲取校驗碼，調用Auth並返回成功後調用此函數可獲取返回的校驗碼。

        :return:    string 與註冊碼相對應的校驗碼。
        '''
        GetCode = self._dll.GetCode
        GetCode.restype = c_char_p
        return GetCode().decode('utf-8')

    def get_ver(self) -> str:
        '''
        Get VLM-Version

        :return:    VLM-Version
        '''
        get_ver = self._dll.GetVer
        get_ver.restype = c_char_p
        return get_ver()

    def init(self):
        '''
        初始化

        :return:    大於等於0表示成功。（連接了某台伺服器並返回伺服器編號），小於0表示連接失敗。失敗時應提示使用者無法連接驗證服務器並退出程序
        '''

        return self._dll["Initialize"](ctypes.c_char_p(self.soft_code.encode('utf-8'))) >= 0

    def user_auth(self, account: str, pwd: str):
        '''
        使用者登入驗證

        :param account: string登入的帳號
        :param pwd: string登入的密碼
        :return:    0 成功 -1 失敗 -2 註冊碼被禁用 -3 綁定機器超限 -4 註冊碼已在線 -5 已過期 -6 使用者餘額不足 -7 使用者無效
        '''
        return self._dll["UserAuth"](ctypes.c_char_p(account.encode('utf-8')), ctypes.c_char_p(pwd.encode('utf-8')))

    def auth(self, auth_code: str):
        '''
        驗證註冊碼是否有效。
        試用卡：是産品編號，則當作測試 用卡處理。
        :param auth_code:   string字串註冊碼，所需驗證的註冊碼。
        :return: 0 成功 -1 失敗 -2 註冊碼被禁用 -3 綁定機器超出數量 -4 註冊碼已在線 -5 已過期
        '''
        auth_res = self._dll["Auth"](ctypes.c_char_p(auth_code.encode('utf-8')))
        self.auth_code = auth_code
        return auth_res

    def auth_trial(self):
        '''
        測試用使用者
        :return:  0 成功 -1 失敗 -2 註冊碼被禁用 -3 綁定機器超出數量 -4 註冊碼已在線 -5 已過期
        '''
        return self.auth(self.soft_code)

    def encrypt(self, type, encode_bytes, key):
        '''
        對GUID字串進行加密

        :param type:    int 0 表示AES算法，1表示MD5算法
        :param encode_bytes:    GUID字串，需要加密的字串
        :param key: 加密鍵值 type 為1(MD5)加密時此參數無意義
        :return:    加密結果，GUID格式的字串
        '''
        encrypt = self._dll.Encrypt
        encrypt.restype = c_char_p
        return encrypt(type, ctypes.c_char_p(encode_bytes.encode('utf-8')),
                       ctypes.c_char_p(key.encode('utf-8'))).decode('utf-8')

    def decrypt(self, type, encode_bytes, key):
        '''

        :param type:    0 表示AES 算法，1 表示MD5 算法
        :param encode_bytes:    GUID字串，需要解密的字串 key string 加密鍵值
        :param key: 為1(MD5) 時此參數無意義
        :return:    解密結果，GUID格式的字串
        '''
        decrypt = self._dll.Decrypt
        decrypt.restype = c_char_p
        result = decrypt(type, ctypes.c_char_p(encode_bytes.encode('utf-8')),
                         ctypes.c_char_p(key.encode('utf-8'))).decode('utf-8')
        return result

    def get_validity(self):
        get_validity = self._dll.GetValidity
        get_validity.restype = c_char_p
        get_validity_str = get_validity().decode('utf-8')
        return get_validity_str

    def update(self, cmd=""):
        return self._dll.Update(cmd)

    def change_password(self, old_password, new_password):
        '''
        使用者密碼修改

        :param old_password:    舊密碼(長度為6~15)
        :param new_password:    新密碼(長度為6~15)
        :return: int 0 表示成功 非0失敗
        '''
        return self._dll["ChangePassword"](ctypes.c_char_p(old_password.encode('utf-8')),
                                           ctypes.c_char_p(new_password.encode('utf-8'))) == 0

    def get_user_type(self):
        '''
        獲取使用者類型，0～15，含義由作者自己定義，在使用者模式下驗證成功方可調用

        :return:    int 獲取使用者類型，0～15，含義由作者自己定義
        '''
        return self._dll["GetUserType"]()

    def user_register(self, account: str, pwd: str, type: int, bind: int, multi: int, point: int):
        '''
        使用者註冊

        :param account: string 使用者名 (長度：6-15)
        :param pwd: string 使用者密碼 (長度：6-15)
        :param type:    int 使用者類型 (範圍：0-15)
        :param bind:    int 是否綁機 (範圍：0-5 ；0為不綁機,7等於通道數)
        :param multi:   int 通道 (範圍：1-200)
        :param point:   int 點數 (範圍：0-8000)
        :return:    int 0 成功 ；-1 失敗 ；-8 使用者名重複
        '''
        account = ctypes.c_char_p(account.encode('utf-8'))
        pwd = ctypes.c_char_p(pwd.encode('utf-8'))
        result = self._dll["UserRegister"](account, pwd, type, bind, multi, point)
        return result

    def add_time(self, card: str, buyer: str, super: str):
        '''
        給使用者帳號加時或註冊卡加時

        :param card:    string 加時卡卡號
        :param buyer:   string 購買編號(使用者名或註冊碼)
        :param super:   string 推薦者帳號(必須為使用者名)
        :param days:    int 天數 此參數按引用傳址，如果加時成功，則返回增加的天數
        :param point:   int 點數 此參數按引用傳址，如果加時成功，則返回增加的點數
        :return:    0 成功，-1 不存在，-7 無效：已被使用或非加時卡（比如:註冊碼）等等
        '''
        card = ctypes.c_char_p(card.encode('utf-8'))
        buyer = ctypes.c_char_p(buyer.encode('utf-8'))
        super = ctypes.c_char_p(super.encode('utf-8'))

        mask = ctypes.c_uint32()
        net = ctypes.c_int32()

        return self._dll["AddTime"](card, buyer, super, ctypes.byref(net), ctypes.byref(mask))

    def unbind(self):
        '''
        對此機器進行解綁操作，在驗證成功後方可調用。

        :return:    0:成功 非0失敗
        '''

        return self._dll.Unbind()

    def release(self):
        '''
        調用此函數VLM將停止工作，用於關閉Process前調用（必須調用否則有機率卡死）。

        :return: 無返回值
        '''
        self._dll.Release()

    def is_valid(self):
        '''
        檢查是否到了無效狀態，這函數是為無法回響COM事件的語言比如易語言裡使用的，每隔幾秒調用一次，在可以回響COM事件的語言裡無需此函數，回響OnInvalid事件即可。

        :return:    Bool true:有效 false:無效
        '''
        return self._dll.IsValid()

    def deduct_hour(self, hours: int):
        '''
        扣除時間

        :param hours:   int 需要扣除的時間 (單位:小時)
        :return:    int 成功 返回0 失敗返回非0
        '''
        return self._dll.DeductHour(hours)

    def deduct_point(self, point: int):
        '''
        扣取點數

        :param point:   int 要扣除的點數
        :return:    int 反回剩餘點數
        '''
        return self._dll.DeductPoint(point)

    def rename(self, dll_name: str = None):
        if not dll_name:
            dll_extension = Path(self._dll_path).stem
        else:
            dll_extension = dll_name.replace('.dll')
        self._dll["Rename"](dll_extension.encode('utf-8'))

    def leave_msg(self, type, msg):
        '''

        :param type:
        :param msg:
        :return:
        '''
        self._dll.LeaveMsg(type, ctypes.c_char_p(msg.encode('utf-8')))


if __name__ == '__main__':

    Vbox = VLM_security(r"C:\Windows\VAuth.dll", "508A142E-83D8-4FCE-A071-825381E9C0E5")

    result = Vbox.init()
    if not result:
        exit()
    return_value = Vbox.get_ver()

    # 測試卡
    reasylt = Vbox.auth_trial()
    # 使用者與註冊碼模式，可以獨立使用或者混和
    # 註冊碼模式
    result = Vbox.auth('279BB3F9-5AB3-4D20-819D-4D24A6408EF0')

    # return_value = Vbox.add_time("15F8D3F0-474B-4124-B5EF-67B59F15A50A","279BB3F9-5AB3-4D20-819D-4D24A6408EF0","test123")
    # 使用者模式
    #
    # Vbox.user_register("testvlm", 'bbb123456', 0, 0, 1, 1000)
    # return_value = Vbox.user_auth("test123", "test456")
    # Vbox.change_password("test456", "test789")
    # return_value = Vbox.get_user_type()
    # return_value = Vbox.get_validity()
    # Vbox.update()
    # return_value = Vbox.is_valid()
    # return_value = Vbox.unbind()
    # return_value = Vbox.deduct_point(10)
    # return_value = Vbox.deduct_hour(5)
    #

    print(return_value)
    Vbox.check_correct()
    Vbox.leave_msg(0, "123123123")
    t = Vbox.decrypt(0, Vbox.get_code(), "123")
    Vbox.release()
    exit()
