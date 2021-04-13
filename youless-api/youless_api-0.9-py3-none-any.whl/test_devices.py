import unittest
import datetime

from unittest.mock import patch, Mock
from youless_api.devices import LS120, LS110
from youless_api.const import STATE_OK, STATE_FAILED


class LS120Tests(unittest.TestCase):

    def test_ls120_failed(self):
        """Check what happens if the remote device is not ok"""
        with patch('youless_api.devices.requests.get') as mock_get:
            mock_get.return_value = Mock(ok=False)

            api = LS120('', {})
            api.update()

        self.assertEqual(api.state, STATE_FAILED)

    def test_ls120_ok(self):
        """Test the update functionality"""
        with patch('youless_api.devices.requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = [{
                "tm": 1611929119,
                "net": 9194.164,
                "pwr": 2382,
                "ts0": 1608654000,
                "cs0": 0.000,
                "ps0": 0,
                "p1": 4703.562,
                "p2": 4490.631,
                "n1": 0.029,
                "n2": 0.000,
                "gas": 1624.264,
                "gts": int(datetime.datetime.now().strftime("%y%m%d%H00"))
            }]

            api = LS120('', {})
            api.update()

        self.assertEqual(api.state, STATE_OK)
        self.assertEqual(api.power_meter.total.value, 9194.164)
        self.assertEqual(api.power_meter.high.value, 4490.631)
        self.assertEqual(api.power_meter.low.value, 4703.562)
        self.assertEqual(api.current_power_usage.value, 2382)
        self.assertEqual(api.gas_meter.value, 1624.264)
        self.assertEqual(api.delivery_meter.high.value, 0.000)
        self.assertEqual(api.delivery_meter.low.value, 0.029)
        
    def test_ls120_stale(self):
        """Test case for incident with stale data from the API"""
        with patch('youless_api.devices.requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = [{
                "tm": 1611929119,
                "net": 9194.164,
                "pwr": 2382,
                "ts0": 1608654000,
                "cs0": 0.000,
                "ps0": 0,
                "p1": 4703.562,
                "p2": 4490.631,
                "n1": 0.029,
                "n2": 0.000,
                "gas": 1624.264,
                "gts": 3894900
            }]

            api = LS120('', {})
            api.update()

        self.assertEqual(api.state, STATE_FAILED)


class LS110Test(unittest.TestCase):

    def test_ls110_ok(self):
        with patch('youless_api.devices.requests.get') as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = {
                "cnt": "141950,625",
                "pwr": 750,
                "lvl": 90,
                "dev": "(&plusmn;3%)",
                "det": "",
                "con": "OK",
                "sts": "(33)",
                "raw": 743
            }

            api = LS110('')
            api.update()

        self.assertEqual(api.state, STATE_OK)
        self.assertEqual(api.power_meter.high.value, None)
        self.assertEqual(api.power_meter.low.value, None)
        self.assertEqual(api.power_meter.total.unit_of_measurement, "W")
        self.assertEqual(api.power_meter.total.value, "141950,625")
        self.assertEqual(api.current_power_usage.value, 750)

