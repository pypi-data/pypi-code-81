from thanetwffapi.simple import pandas_func, input_test

class TestTestSimple:
    def test_pandas_func(self):
        assert pandas_func()['Name'][0] == 'Alex'

    def test_input_test(self):
        input_result = input_test(10)
        assert input_result == 20