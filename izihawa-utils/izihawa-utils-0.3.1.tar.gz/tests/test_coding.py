import unittest

from izihawa_utils.coding import (
    base58_check_decode,
    base58_check_encode,
    base58_decode,
    base58_encode,
    base256_decode,
    base256_encode,
    count_leading_chars,
)


class TestCoding(unittest.TestCase):
    def test_count_leading_characters(self):
        self.assertEqual(count_leading_chars('a\0bcd\0', '\0'), 0)
        self.assertEqual(count_leading_chars('\0\0a\0bcd\0', '\0'), 2)
        self.assertEqual(count_leading_chars('1a\0bcd\0', '1'), 1)

    def test_base256(self):
        self.assertEqual(base256_encode(base256_decode(b'abc')), b'abc')
        self.assertEqual(base256_encode(0x4142), b'AB')
        self.assertEqual(base256_decode(b'AB'), 0x4142)

    def test_base58(self):
        self.assertEqual(base58_encode(base58_decode('abc')), 'abc')
        self.assertEqual(base58_decode('121'), 58)
        self.assertEqual(base58_decode('5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ'),
                         0x800C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D507A5B8D)

    def test_base58_check(self):
        self.assertEqual(base58_check_decode(base58_check_encode(b'abc', 42)), (b'abc', 42))
        self.assertEqual(base58_check_decode(base58_check_encode(b'\0\0abc', 0)), (b'\0\0abc', 0))
        s = base256_encode(0x0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D)
        b = base58_check_encode(s, 0x80)
        self.assertEqual(b, "5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ")
