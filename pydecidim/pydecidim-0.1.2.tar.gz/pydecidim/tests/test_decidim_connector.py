import unittest

from pydecidim.api.decidim_connector import DecidimConnector

QUERY_PATH = "https://www.decidim.barcelona/api"


class DecidimConnectrTest(unittest.TestCase):
    def test_execute_query(self):
        decidim_reader: DecidimConnector = DecidimConnector(QUERY_PATH)
        response = decidim_reader.execute_query("{decidim {version}}")
        self.assertIsInstance(response, dict)
        self.assertTrue('decidim' in response)

    def test_execute_query_from_file(self):
        decidim_reader: DecidimConnector = DecidimConnector(QUERY_PATH)
        response = decidim_reader.execute_query_from_file('../queries/version.graphql')
        self.assertIsInstance(response, dict)
        self.assertTrue('decidim' in response)


if __name__ == '__main__':
    unittest.main()
