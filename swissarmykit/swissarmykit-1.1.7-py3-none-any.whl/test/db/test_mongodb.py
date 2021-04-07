from unittest import TestCase

from swissarmykit.db.mongodb import BaseDocument
test = BaseDocument.get_class('test')


class TestMongodb(TestCase):

    def setUp(self) -> None:
        pass

    def test_get(self):
        for i in range(0, 20):
            test.save_url(str(i), name='name_' + str(i), attr={'ranking': 1})
            print('.', end='', flush=True)

        for item in test.get_one(10, offset=0, order_by=['-ranking', '-id']):
            print(item)
        print('-------------')
        for item in test.get_one(10, offset=10, order_by=['-ranking', '-id']):
            print(item)
        print('-------------')
        for item in test.get_one(20, offset=0, order_by=['-ranking', '-id']):
            print(item)

    def test_increment(self):
        # for item in test.get_one(10, offset=10):
        #     print(item.increment())

        print(test.inc_counter('5fa63ff48135b182f50f0693'))