import unittest

from pydecidim.api.comment_reader import CommentReader
from pydecidim.api.decidim_connector import DecidimConnector
from pydecidim.model.comment import Comment

QUERY_PATH = "https://www.decidim.barcelona/api"


class ProposalReaderTest(unittest.TestCase):
    def test_execute_not_exists(self):
        decidim_connector: DecidimConnector = DecidimConnector(QUERY_PATH)
        reader: CommentReader = CommentReader(decidim_connector, base_path="../..")
        # We use the participatory process #40 on Decidim.org api and the Proposal #12045
        comment: Comment = reader.execute("40", "12040", "2", d)
        self.assertIsNone(comment)

    def test_execute_exists(self):
        decidim_connector: DecidimConnector = DecidimConnector(QUERY_PATH)
        reader: CommentReader = CommentReader(decidim_connector, base_path="../..")
        # We use the participatory process #40 on Decidim.org api and the Proposal #12040
        comment: Comment = reader.execute("40", "12045", "19657", d)
        self.assertIsInstance(comment, Comment)


if __name__ == '__main__':
    unittest.main()
