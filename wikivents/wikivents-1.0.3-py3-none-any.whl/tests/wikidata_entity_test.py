import os
import pickle
import unittest
from copy import copy
from unittest.mock import patch, Mock

from wikivents.models import WikidataEntity, EntityType


class TestWikidataEntity(unittest.TestCase):

    def setUp(self) -> None:
        self.barack_obama_id_name_tuple = ("Q76", "human_barack_obama")

    @patch("wikivents.wikidata.WikidataClient")
    def test_barack_obama_url(self, wikidata_client_mock):
        barack_obama_entity = self._get_barack_obama_entity(wikidata_client_mock)
        self.assertEqual("https://wikidata.org/wiki/Q76", barack_obama_entity.url)

    @patch("wikivents.wikidata.WikidataClient")
    def test_barack_obama_label_in_english(self, wikidata_client_mock):
        barack_obama_entity = self._get_barack_obama_entity(wikidata_client_mock)
        self.assertEqual("Barack Obama", barack_obama_entity.label.get("en"))

    @patch("wikivents.wikidata.WikidataClient")
    def test_barack_obama_names(self, wikidata_client_mock):
        barack_obama_entity = self._get_barack_obama_entity(wikidata_client_mock)
        self.assertEqual(
            barack_obama_entity.names(),
            {'Barak Obama', 'Obama', 'Barack', 'BHO', 'President Barack Obama', 'Barry Obama',
             'Barack Obama', 'Barack Hussein Obama', 'Barack Hussein Obama II', 'Barack Obama II',
             'President Obama'}
        )

    @patch("wikivents.wikidata.WikidataClient")
    def test_barack_obama_repr(self, wikidata_client_mock):
        barack_obama_entity = self._get_barack_obama_entity(wikidata_client_mock)
        self.assertEqual(
            f"<WikidataEntity ({barack_obama_entity.id}, {barack_obama_entity.label.get('en')})>",
            barack_obama_entity.__repr__()
        )

    @patch("wikivents.wikidata.WikidataClient")
    def test_barack_obama_str(self, wikidata_client_mock):
        barack_obama_entity = self._get_barack_obama_entity(wikidata_client_mock)
        self.assertEqual(barack_obama_entity.label.get('en'), barack_obama_entity.__str__())

    @patch("wikivents.wikidata.WikidataClient")
    def test_barack_obama_eq(self, wikidata_client_mock):
        barack_obama_entity = self._get_barack_obama_entity(wikidata_client_mock)
        barack_obama_entity_copy = copy(barack_obama_entity)
        self.assertEqual(barack_obama_entity.id, barack_obama_entity_copy.id)
        self.assertEqual(barack_obama_entity, barack_obama_entity_copy)

    @patch("wikivents.wikidata.WikidataClient")
    def test_barack_obama_neq(self, wikidata_client_mock):
        barack_obama_entity = self._get_barack_obama_entity(wikidata_client_mock)
        barack_obama_entity_copy = copy(barack_obama_entity)
        barack_obama_entity_copy.id += "0"
        self.assertNotEqual(barack_obama_entity.id, barack_obama_entity_copy.id)
        self.assertNotEqual(barack_obama_entity, barack_obama_entity_copy)

    @patch("wikivents.wikidata.WikidataClient")
    def test_barack_obama_hash(self, wikidata_client_mock):
        barack_obama_entity = self._get_barack_obama_entity(wikidata_client_mock)
        self.assertEqual(hash(barack_obama_entity.id), barack_obama_entity.__hash__())

    @patch("wikivents.wikidata.WikidataQueryHandler")
    @patch("wikivents.wikidata.WikidataClient")
    def test_barack_obama_type(self, wikidata_client_mock, wikidata_query_handler_mock):
        barack_obama_entity = self._get_barack_obama_entity(wikidata_client_mock, wikidata_query_handler_mock)
        self.assertEqual(EntityType.PERSON, barack_obama_entity.type)

    def _get_barack_obama_entity(self, wikidata_client_mock, wikidata_query_handler_mock=None):
        with open(self._get_entity_file_path(*self.barack_obama_id_name_tuple), mode="rb") as entity_data_file:
            wikidata_client_mock.request = Mock(return_value=pickle.load(entity_data_file))
            if wikidata_query_handler_mock:
                wikidata_query_handler_mock.get_all_entities_ids_the_entity_id_is_an_instance_of = Mock(
                    return_value={'Q5', 'Q26720107', 'Q45983014', 'Q99527517'}  # and more others
                )
                return WikidataEntity(self.barack_obama_id_name_tuple[0], wikidata_client_mock)
            return WikidataEntity(self.barack_obama_id_name_tuple[0], wikidata_client_mock)

    @staticmethod
    def _get_entity_file_path(entity_id: str, entity_label: str):
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", f"{entity_id}_{entity_label}_request_data.pickle"
        )


if __name__ == '__main__':
    unittest.main()
