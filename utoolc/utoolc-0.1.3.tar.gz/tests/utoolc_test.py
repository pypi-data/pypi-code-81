import unittest
import utoolc


# 创建Test基础类BaseModuleTest
class BaseModuleTest(unittest.TestCase):
    def test(self):
        utoolc.utils.print_a_line()
        print(utoolc.get_random.get_random_str_with_counts(5))
        print(utoolc.__version__)
        print(utoolc.utils.get_now_time())
        utoolc.utils.print_a_line()
        self.assertEqual(1, 1)

    def test2(self):
        self.assertNotEqual(1, 2)

    def test3(self):
        print('测试其他...')
        self.assertEqual(1, 1)

    def test4(self):
        utoolc.easy_say.say_hello_world('LC')


if __name__ == '__main__':
    unittest.main()
