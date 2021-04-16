"""64 bit Fnv-1a hash module"""


class FNV1a:
    """
    64 Bit FNV-1a Hashing Algorithm:

    http://www.isthe.com/chongo/tech/comp/fnv/index.html#FNV-1a

    s/n = seed/offset/hashed value
    t = text string
    c = character in string
    p = 64 bit prime (2**40 + 2**8 + 0xb3)
    m = 64 bit bitmask
    h = final 64 bit hash value

    HASH:
    t = ( c_1 + c_2 + ... + c_x )
    n_1 = s
    n_2 = ( n_1 ^ c_1 ) * p
    n_x = ( n_(x-1) ^ c_(x-1) ) * p
    h = n_x & m

    DEHASH FROM HASH LIST:
    c_x = ( n_x // p ) ^ n_(x-1)
    c_2 = ( n_2 // p ) ^ n_1
    c_1 = ( n_1 // p ) ^ s
    t = ( c_1 + c_2 + ... + c_x )
    ...

    USAGE:
        >>> from fnv1a import FNV1a
        >>>
        >>> hasher = FNV1a()
        >>> hasher
        FNV1a(seed=14695981039346656037, prime=1099511628211,
         mask=18446744073709551615, text=None, hash_out=None, hash_list=[])
        >>>
        >>> hasher.hash("This is a test.com bro.")
        'ade2f4095d74bf44'
        >>>
        >>>
        >>> new_hasher = FNV1a()
        >>> new_hasher
        FNV1a(seed=14695981039346656037, prime=1099511628211,
         mask=18446744073709551615, text=None, hash_out=None, hash_list=[])
        >>>
        >>> new_hasher.dehash(hasher.hash_list)
        'This is a test.com bro.'
        >>>
    """
    _seed = 14695981039346656037
    _prime = 1099511628211
    _mask = 0xFFFFFFFFFFFFFFFF

    def __init__(self):
        self.hash_list = []
        self.hash_out = None
        self.text = None

    def __repr__(self):
        return ('{}(seed={}, prime={}, mask={}, text={}, '
                'hash_out={}, hash_list={})').format(self.__class__.__name__,
                                                     self._seed, self._prime,
                                                     self._mask, self.text,
                                                     self.hash_out,
                                                     self.hash_list)

    def hash(self, text: str) -> str:
        """Creates a 64 bit hash from a string input."""
        n_x, prime, mask = self._seed, self._prime, self._mask
        self.hash_list = []
        hash_list = self.hash_list
        self.text = str(text)
        for char in self.text:
            n_x = (n_x ^ ord(char)) * prime
            hash_list.append(n_x)
        self.hash_out = hex(n_x & mask)[2:]
        hash_list.append(self._seed)
        return self.hash_out

    def _clear(self):
        """Clear variabels from instance."""
        self.hash_list = []
        self.hash_out = None
        self.text = None

    def _type_check(self, value, value_type):
        """Check hash_array types"""
        if not isinstance(value, value_type):
            self._clear()
            raise TypeError("Must supply a list of integers")

    def dehash(self, hash_list: list = None) -> str:
        """Dehashes/reverts a hash list used to build a hash and returns the
         original string."""
        prime, out = self._prime, []
        self._type_check(hash_list, list)
        if not hash_list:
            if not self.hash_list:
                self._clear()
                return None
            hash_list = self.hash_list
        self._type_check(hash_list[0], int)
        try:
            for i in range(len(hash_list) - 1)[::-1]:
                self._type_check(i, int)
                char = (hash_list[i] // prime) ^ hash_list[i - 1]
                out.append(chr(char))
                self.text = ''.join(out[::-1])
        except (OverflowError, ValueError) as error:
            self._clear()
            raise ValueError("Invalid input, could not be dehashed") from error
        self.hash_out, self.hash_list = FNV1a().hash(self.text), hash_list
        return self.text
