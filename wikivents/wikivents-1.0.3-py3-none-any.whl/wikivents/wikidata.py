#!/usr/bin/env python3
#
# Copyright (C) 2020 Guillaume Bernard <contact@guillaume-bernard.fr>
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
from collections import defaultdict
from typing import List, Dict, Tuple, Set

from SPARQLWrapper import SPARQLWrapper, JSON
from jinja2 import Template
from wikidata.client import Client
from wikidata.entity import EntityId, Entity

from wikivents import logger


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class WikidataClient(Client, metaclass=Singleton):
    """
    The Wikipedia package Client as a Singleton.
    """


class WikidataQueryHandler(metaclass=Singleton):
    """
    Query the Wikidata SPARQL endpoint and retrieve entities and objects, usable in the models modules.
    """

    user_agent = "Wikidata Python export/0.1 (https://gitlab.com/guilieb/wikivents)"
    endpoint_url = "https://query.wikidata.org/sparql"

    def __init__(self):
        self._wikidata_client = Client()
        self._sparql_wrapper = SPARQLWrapper(WikidataQueryHandler.endpoint_url, agent=WikidataQueryHandler.user_agent)
        self._sparql_wrapper.setReturnFormat(JSON)

    def _raw_query_select_results(self, raw_sparql_query: str) -> Dict[EntityId, Dict[EntityId, Set[str]]]:
        """
        Run an raw SPARQL query against the Wikidata Query Service and transform the results into a Python structure

        The results will be stored in a Python dictionary. The key of this dictionary is the Wikidata id.
        As value, it contains another dictionary with the properties and the corresponding values.
        For instance, if the entity has multiple “is-instance” values, the key of this dictionary will be P31 (the
        property ID that corresponds to “is-instance” and the list of Wikidata identifiers as value.

        :param raw_sparql_query: the raw SPARQL query to run against the Wikidata SPARQL service.
        :return: the query results, as a dictionary (described above)
        """
        self._sparql_wrapper.setQuery(raw_sparql_query)
        sparql_query_response_results = self._sparql_wrapper.query().convert().get("results").get("bindings")
        return self._convert_query_results_into_python_structure(sparql_query_response_results)

    # noinspection PyMethodMayBeStatic
    def _convert_query_results_into_python_structure(
        self, sparql_query_response_results: List[Dict[str, Dict[str, str]]]
    ) -> Dict[EntityId, Dict[EntityId, Set[str]]]:
        """
        A list of Wikidata SPARQL query results. Each element is a dictionary, with, as keys, the SELECT
        parameters. Each value has a RDF “datatype”, a “type” and a “value”, themselves stored in a dictionary.

        For instance:
        .. code-block:: javascript
            {
                item': {
                    'type': 'uri',
                    'value': 'http://www.wikidata.org/entity/Q4560206'
                },
            }

        :param sparql_query_response_results: the “bindings” value of the query result provided by the SPARQLWrapper
        module.
        :return: a dictionary that contains entity identifiers as keys, the value being the property identifier
        and the corresponding values.
        """
        entities_with_properties = defaultdict(lambda: defaultdict(set))
        for sparql_query_result in sparql_query_response_results:
            # ’item’ key stores the Wikidata element URL: https://www.wikidata.org/wiki/Q26
            wikidata_entity_id = EntityId(sparql_query_result.get("item").get("value").split("/")[-1])
            del sparql_query_result["item"]

            for wikidata_item_property, wikidata_item_value in sparql_query_result.items():
                entities_with_properties[wikidata_entity_id][wikidata_item_property].add(wikidata_item_value)

        return entities_with_properties

    def query_wikidata_endpoint_from_sparql_query_string(self, sparql_query: str) -> Set["EntityId"]:
        """
        Query the Wikidata SPARQL API from a query string.

        :return: a collection that contains the found entity ids
        """
        logger.debug("Querying entities from string: ‘%s’", sparql_query.replace("\n", " "))

        query_result_entity_ids = set()
        raw_query_results = self._raw_query_select_results(sparql_query)

        counter, total = 0, len(raw_query_results)
        for entity_id in raw_query_results:
            logger.debug("Fetching entity %s/%s: %s…", counter, total, entity_id)
            query_result_entity_ids.add(EntityId(entity_id))
            counter += 1
        return query_result_entity_ids

    def query_wikidata_endpoint_from_jinja_template_query(self, template_filename: str, **kwargs) -> Set["EntityId"]:
        """
        Query the Wikidata SPARQL API from a Jinja template. Jinja template keyword arguments are stored in kwargs.

        :return: a dict which contains the entity identifier and the corresponding entity object as value.
        """
        logger.info("Querying entities from template ‘%s’", template_filename)
        with open(template_filename, encoding="utf-8") as template_file:
            return self.query_wikidata_endpoint_from_sparql_query_string(Template(template_file.read()).render(kwargs))

    def is_entity_id_an_instance_of(self, entity_id: "EntityId", instance_of: "EntityId") -> bool:
        """
        Check whether an entity id corresponds to an element which is an instance of another entity id.

        :param entity_id: the entity id of the entity to check
        :param instance_of: the entity of the entity that represent the type that’s checked
        """
        self._sparql_wrapper.setQuery(
            f"""ASK WHERE {{
                wd:%{entity_id} wdt:P31 ?instance_of.
                ?instance_of wdt:P279* ?mid.
                ?mid wdt:P279* ?element_classes.
                FILTER (wd:%{instance_of} IN (?element_classes))
            }}"""
        )
        return bool(self._sparql_wrapper.query().convert().get("boolean"))

    def get_all_entities_the_entity_id_is_an_instance_of(self, entity_wikidata_id: "EntityId") -> Set["Entity"]:
        """
        Get all instance_of Entities of the Entity in parameter. For instance, it returns all the
        objects of a certain instance_of value.

        :param entity_wikidata_id: the entity identifier
        :return: the list of entities that are instance of entity id. For instance, for the event id Q193689 (Q193689
            is “Easter Rising”), values are [<Wikidata.Entity instance: Q124734>]. (Q124734 is “rebellion”)
        """
        wikidata_entities_instances = set()
        entity_ids = self.get_all_entities_ids_the_entity_id_is_an_instance_of(entity_wikidata_id)

        counter, total = 0, len(entity_ids)
        for result_entity_id in entity_ids:
            logger.debug("Fetching entity %d/%d : %s…", counter, total, result_entity_id)
            wikidata_entities_instances.add(WikidataClient().get(result_entity_id, load=True))
            counter += 1

        return wikidata_entities_instances

    def get_all_entities_ids_the_entity_id_is_an_instance_of(self, entity_wikidata_id: "EntityId") -> Set["EntityId"]:
        """
        Get all instance_of values of the Entity represented by its identifier given in parameter

        :param entity_wikidata_id: the element for which to get instance_of values.
        :return: the list of entity identifiers that the given entity is an instance of. For instance, for the event id
            Q193689 (Q193689 is “Easter Rising”), values are ['Q124734']. (Q124734 is “rebellion”)
        """
        self._sparql_wrapper.setQuery(
            f"""SELECT ?element_class (COUNT(?mid) AS ?depth) WHERE {{
                wd:{entity_wikidata_id} wdt:P31 ?instance_of.
                ?instance_of wdt:P279* ?mid.
                ?mid wdt:P279* ?element_class.
            }} GROUP BY ?element_class
            ORDER BY ?depth"""
        )
        return {
            element_class.get("element_class").get("value").split("/")[-1]
            for element_class in self._sparql_wrapper.query().convert().get("results").get("bindings")
        }

    def get_all_entities_instance_of_wikidata_id_in_time_interval(
        self, wikidata_instance_id: EntityId, date_range: Tuple[str, str] = ("1850-01-01", "1950-12-31")
    ) -> Set[Entity]:
        """
        Get the list of entities identifiers that are of a specific instance, identified by the given parameter.

        :param wikidata_instance_id: the instance identifier
        :param date_range: a tuple with two date strings (ISO-8601) representing the starting date range, and the
            ending date. For instance: ("1850-01-01", "1950-12-31").
        :return: the list of entities identifiers that are instances of the given id. For instance, if the input is
            Q124734 (Q124734 is “rebellion”), the values are [<Wikidata.Entity instance: Q193689>, …] which are
            rebellion entities.
        """
        entities = set()
        entity_ids = self.get_all_entities_ids_instance_of_wikidata_id_in_time_interval(
            wikidata_instance_id, date_range
        )

        counter, total = 0, len(entity_ids)
        for result_entity_id in entity_ids:
            logger.debug("Fetching entity %d/%d : %s…", counter, total, result_entity_id)
            entities.add(WikidataClient().get(result_entity_id, load=True))
            counter += 1

        return entities

    def get_all_entities_ids_instance_of_wikidata_id_in_time_interval(
        self, wikidata_instance_of_id: "EntityId", date_range: Tuple[str, str] = ("1850-01-01", "1950-12-31")
    ) -> Set["EntityId"]:
        """
        Get the list of entities identifiers that are of a specific instance, identified by the given parameter.

        :param wikidata_instance_of_id: the instance identifier of something like ’rebellion’ or ‘ceremony’.
        :param date_range: a tuple with two date strings (ISO-8601) representing the starting date range, and the
            ending date. For instance: ("1850-01-01", "1950-12-31").
        :return: the list of entities identifiers that are instances of the given id. For instance, if the input is
            Q124734 (Q124734 is “rebellion”), the values are ['Q130713', 'Q183959', 'Q188613'] which are rebellion
            entities.
        """
        self._sparql_wrapper.setQuery(
            f"""SELECT DISTINCT ?item WHERE {{
                ?item wdt:P31/wdt:P279* wd:{wikidata_instance_of_id}.
                ?item wdt:P585 ?date.
                FILTER(("{date_range[0]}"^^xsd:dateTime <= ?date) && (?date < "{date_range[1]}"^^xsd:dateTime))
            }}
            """
        )
        return {
            element_class.get("item").get("value").split("/")[-1]
            for element_class in self._sparql_wrapper.query().convert().get("results").get("bindings")
        }
