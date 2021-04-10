import base64
class EncoderSIC(object):
    def __init__(self, **kwargs):
        """
        get or set macaddress, computername and username.
        """
        from uuid import getnode as get_mac
        import os
        self.secret_key = 'Mtfp5BsFL)T^aM/W-mHrY5rDzuX6(YbPTLpHxAU?YbF9g?BbtWH2dt'
        self.mac = kwargs.get('macaddress', get_mac())
        self.computer_name = kwargs.get('computername', os.getenv('COMPUTERNAME'))
        self.user_name = kwargs.get('username', os.getenv('USERNAME'))
        self.encrypt()
        
    def encode(self, key, clear):
        enc = []
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        enc_str=("".join(enc)).encode(encoding='UTF-8')
        return base64.urlsafe_b64encode(enc_str)
    def decode(self, key, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc)
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(chr(enc[i])) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)
    def encrypt(self):
        computer_name_ll = self.computer_name[len(self.computer_name)-1:len(self.computer_name)]
        computer_name_fls = self.computer_name[0:len(self.computer_name)-1]
        return self.encode(self.secret_key, "%s%s%s%s"%(computer_name_ll, self.mac, self.user_name, computer_name_fls))
    def decrypt(self, enc):
        return self.decode(self.secret_key, enc)
    def encrypt_key_and_apps(self, key=None, apps=''):
        value = self.decrypt(key)
        return self.encode(self.secret_key, "%s|%s"%(value,apps))
