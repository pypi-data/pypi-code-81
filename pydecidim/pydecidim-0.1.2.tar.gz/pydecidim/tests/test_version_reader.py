import unittest

from pydecidim.api.decidim_connector import DecidimConnector
from pydecidim.api.version_reader import VersionReader

QUERY_PATH = "https://www.decidim.barcelona/api"


class VersionReaderTest(unittest.TestCase):
    def test_execute(self):
        decidim_connector: DecidimConnector = DecidimConnector(QUERY_PATH)
        version_reader: VersionReader = VersionReader(decidim_connector, base_path="../..")
        version = version_reader.execute()
        self.assertIsInstance(version, str)


if __name__ == '__main__':
    unittest.main()
