"""
Support for Argon2-based hashing
"""

# Built-in library packages
from base64 import b64decode

# Third party packages
from argon2 import low_level

# In project
from phibes.crypto.crypt_ifc import HashIfc


class Argon2ParamObj:
    """
    Helper object for Argon2 hashing
    """
    def __init__(self, argon2_str: str = None, params_dict: dict = None):
        if argon2_str is not None and params_dict is not None:
            raise ValueError(
                'need to pass only one of argon2_str and params_dict'
            )
        elif argon2_str:
            pad = (0, 1)[argon2_str.startswith('$')]
            out_vars = argon2_str.split('$')
            perf_params = out_vars[pad + 2].split(',')
            memory_cost = time_cost = parallelism = None
            for param in perf_params:
                if param.count('=') == 1:
                    start_pos = param.find('=') + 1
                    if param.startswith('m'):
                        memory_cost = int(param[start_pos:])
                    elif param.startswith('t'):
                        time_cost = int(param[start_pos:])
                    elif param.startswith('p'):
                        parallelism = int(param[start_pos:])
            if not (memory_cost and time_cost and parallelism):
                raise ValueError(
                    f'missing param {memory_cost=} {time_cost=} {parallelism=}'
                )
            self.hash_type = out_vars[pad + 0]
            self.version = out_vars[pad + 1]
            self.time_cost = time_cost
            self.memory_cost = memory_cost
            self.parallelism = parallelism
            self.salt = out_vars[pad + 3]
            if len(out_vars) > pad + 4:
                self.hash = out_vars[pad + 4]
        elif params_dict:
            print(f"{params_dict=}")
            self.hash_type = params_dict['hash_type']
            self.version = params_dict['version']
            self.time_cost = params_dict['time_cost']
            self.memory_cost = params_dict['memory_cost']
            self.parallelism = params_dict['parallelism']
            self.salt = params_dict['salt']
            self.hash_len = params_dict['hash_len']
            self.salt_len = params_dict['hash_len']
            self.hash = '?'
        else:
            raise ValueError('need to pass initial values')
        return

    def get_argon2_str(self):
        type_str = f"argon2{self.hash_type.lower()}"
        ver_str = f"v={low_level.ARGON2_VERSION}"
        params = (
            f"m={self.memory_cost},t={self.time_cost},p={self.parallelism}"
        )
        ret_val = (f"${type_str}${ver_str}${params}${self.salt}${self.hash}")
        return ret_val
# '$argon2id$v=19$m=102400,t=2,p=8$HChGfKTcwnA6TSiJTnvN5Q$9jff8g55n2f+URKWcTUVYA'


class HashArgon2(HashIfc):
    """
    Class for Argon2 hashing
    """

    def __init__(self, **kwargs):
        """
        Constructor
        @param kwargs:
        """
        super(HashArgon2, self).__init__(**kwargs)
        self.time_cost = kwargs['time_cost']
        self.memory_cost = kwargs['memory_cost']
        self.parallelism = kwargs['parallelism']
        self.hash_len = kwargs['hash_len']
        self.hash_type = kwargs['hash_type']

    @staticmethod
    def extract_salt_str(argon2hash_output):
        salt = argon2hash_output[4].encode()
        missing_padding = len(salt) % 4
        if missing_padding:
            salt += '=' * (4 - missing_padding)
        return b64decode(salt)

    @staticmethod
    def burst_output_str(argon2hash_output: str):
        """
        Take an argon-cffi hash_secret response, create and return a dict
        :param argon2hash_output:
        :type argon2hash_output:
        :return:
        :rtype:
        """
        return Argon2ParamObj(argon2_str=argon2hash_output)

    def hash_secret(self, secret: str, salt: str):
        ll_result = low_level.hash_secret(
            secret.encode(),
            bytes.fromhex(salt),
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            hash_len=self.hash_len,
            type=self.hash_type
        ).decode()
        print(ll_result)
        # abundance of caution - verify the returned salt
        ll_salt = ll_result.split('$')[4].encode()
        missing_padding = len(ll_salt) % 4
        if missing_padding:
            ll_salt += b'=' * (4 - missing_padding)
        ll_salt = b64decode(ll_salt).hex()
        if not ll_salt == salt:
            print(f"warning, mismatch {ll_salt=} != {salt=}")
        return ll_result
