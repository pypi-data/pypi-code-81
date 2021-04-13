import unittest
from unittest.mock import patch, Mock
from youless_api import YoulessAPI


def mock_ls110_device(*args, **kwargs):
    if args[0] == 'http://192.1.1.1/d':
        return Mock(ok=False)
    if args[0] == 'http://192.1.1.1':
        return Mock(ok=True)

    return Mock(ok=False)


class YoulessAPITest(unittest.TestCase):

    def test_device_ls120(self):
        with patch('youless_api.requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = {'mac': '293:23fd:23'}

            api = YoulessAPI('192.1.1.1')
            api.initialize()

        self.assertEqual(api.model, 'LS120')
        self.assertEqual(api.mac_address, '293:23fd:23')

    @patch('youless_api.requests.get', side_effect=mock_ls110_device)
    def test_device_ls110(self, mock_get):
        api = YoulessAPI('192.1.1.1')
        api.initialize()

        self.assertEqual(api.model, 'LS110')
        self.assertIsNone(api.mac_address)
