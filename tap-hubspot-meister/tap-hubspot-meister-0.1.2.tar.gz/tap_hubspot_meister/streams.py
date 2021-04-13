import json
import os

import singer
from hubspot.crm import ObjectType
from hubspot.crm.associations import BatchInputPublicObjectId
from hubspot.crm.contacts import (
    BatchReadInputSimplePublicObjectId,
    SimplePublicObjectId,
)
from pydash import find
from rich.console import Console
from singer import metadata, metrics, utils

import tap_hubspot_meister.bookmark as bookmark
import tap_hubspot_meister.transform as transform

console = Console()

LOGGER = singer.get_logger()


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def enrich_data(
    self,
    current_bookmark,
    initial_list,
    batch_properties,
    sub_client,
    associations=None,
):
    filtered_elements = []

    # The enrichement of the elements based on Batch API is limited by the fact that the batch API only accepts 100 inputs a time
    # The solution is to filter the elements before they are sent to batch
    for tmp in initial_list:
        create_date = utils.strptime_to_utc(tmp.properties[self.replication_key])
        if create_date > current_bookmark:
            filtered_elements.append(tmp)

    # Split into batches of 100 elements
    batches = chunks(filtered_elements, 100)
    enriched_elements = []

    # Enrichement
    for batch in batches:
        inputs = [SimplePublicObjectId(id=temp.id) for temp in batch]
        if associations is None:
            enriched = sub_client.batch_api.read(
                batch_read_input_simple_public_object_id=BatchReadInputSimplePublicObjectId(
                    inputs=inputs, properties=batch_properties
                )
            )
        else:
            if associations == "deals_companies":
                enriched = sub_client.batch_api.read(
                    ObjectType.DEALS,
                    ObjectType.COMPANIES,
                    batch_input_public_object_id=BatchInputPublicObjectId(
                        inputs=inputs
                    ),
                )
            elif associations == "deals_contacts":
                enriched = sub_client.batch_api.read(
                    ObjectType.DEALS,
                    ObjectType.CONTACTS,
                    batch_input_public_object_id=BatchInputPublicObjectId(
                        inputs=inputs
                    ),
                )
        enriched_elements = enriched_elements + enriched.results
    return enriched_elements


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def get_breadcrumbs(schema):
    """Creates the breadcrumbs of metadata for the streams

    Args:
        schema: JSON schema of the stream

    Returns:
        A list with the breadcrumbs

    Raises : None
    """

    # Create breadcrumbs
    breadcrumbs = []
    # Path to leave in JSON
    path = []

    def flatten(schema, level):
        if isinstance(schema, dict):
            for key, val in schema.items():
                # The first property field must not be visited, so level must be > 0
                if (key == "properties" and level > 0) or key != "properties":
                    if level > 1:
                        path.append("properties")
                    if key == "type" and val == "object":
                        # Drill down each object and add properties to the path in order to follow JSON schema
                        path.append("properties")
                        # Recurtion
                        flatten(schema["properties"], level + 1)
                    else:
                        if val["type"] == "object":
                            # Recursion
                            path.append(key)
                            flatten(val["properties"], level + 1)
                        else:
                            # Last leave of the tree
                            path.append(key)
                            breadcrumbs.append(".".join(path))
                            if level >= 1:
                                # Delete some of the path to add each leave keeping the path until a sibling
                                del path[-level:]
                            else:
                                path.clear()

    # Start recursion
    flatten(schema, 0)
    return breadcrumbs


class Stream:
    name = None
    replication_method = None
    replication_key = None
    key_properties = None
    stream = None

    def __init__(self, client=None, config=None):
        self.client = client
        self.config = config

    def get_bookmark(self, state):
        return utils.strptime_with_tz(
            singer.get_bookmark(state, self.name, self.replication_key)
        )

    def update_bookmark(self, state, value):
        current_bookmark = self.get_bookmark(state)
        if value and utils.strptime_with_tz(value) > current_bookmark:
            singer.write_bookmark(state, self.name, self.replication_key, value)

    def load_schema(self):
        schema_file = "schemas/{}.json".format(self.name)
        with open(get_abs_path(schema_file)) as f:
            schema = json.load(f)
        return schema

    def load_metadata(self):
        schema = self.load_schema()
        mdata = metadata.new()

        mdata = metadata.write(mdata, (), "table-key-properties", self.key_properties)
        mdata = metadata.write(
            mdata, (), "forced-replication-method", self.replication_method
        )

        if self.replication_key:
            mdata = metadata.write(
                mdata, (), "valid-replication-keys", [self.replication_key]
            )

        # Stream selected by default
        mdata = metadata.write(mdata, (), "selected", True)

        breadcrumbs = get_breadcrumbs(schema)
        for breadcrumb in breadcrumbs:
            tmp = tuple(breadcrumb.split("."))
            key_property_present = False
            for item in self.key_properties:
                # key_properties is an array
                if item in tmp:
                    key_property_present = True
            if self.replication_key in tmp or key_property_present:
                mdata = metadata.write(mdata, tmp, "inclusion", "automatic")
            else:
                mdata = metadata.write(mdata, tmp, "inclusion", "available")
                mdata = metadata.write(mdata, tmp, "selected", True)
                mdata = metadata.write(mdata, tmp, "selected-by-default", True)
        return metadata.to_list(mdata)

    def is_selected(self):
        return self.stream is not None


class Contacts(Stream):
    name = "contacts"
    key_properties = ["hs_object_id"]
    replication_method = "INCREMENTAL"
    replication_key = "lastmodifieddate"

    def sync(self, state):

        LOGGER.info("%s: Starting sync", self.name)

        # Counter
        counter = metrics.Counter("record_count", {"endpoint": self.name})

        # Get the current bookmark
        current_bookmark = bookmark.get_bookmark(self, state)

        # Write the bookmark in the state
        singer.write_bookmark(
            state, self.name, self.replication_key, current_bookmark.isoformat()
        )

        all_contacts = self.client.crm.contacts.get_all()

        # console.log(str(len(all_contacts)) + " contacts", style="bold cyan")

        batch_properties = [
            "firstname",
            "lastname",
            "email",
            "associatedcompanyid",
            "hubspot_owner_id",
            "lifecyclestage",
            "jobtitle",
        ]
        enriched_contacts = enrich_data(
            self,
            current_bookmark,
            all_contacts,
            batch_properties,
            self.client.crm.contacts,
        )

        # console.log(str(len(enriched_contacts)) + " enriched contacts", style="bold cyan")

        for contact in enriched_contacts:
            # Transformation of the data in order to select the right records and STOUT the singer message
            outcome = transform.transform_and_log(
                self, state, contact.properties, self.replication_key, current_bookmark
            )
            if outcome:
                # Only count successful record transformations
                counter.increment()

        # Modify the state
        if self.replication_method == "INCREMENTAL":
            singer.write_state(state)

        LOGGER.info("%s: Completed sync (%s rows)", self.name, counter.value)


class Companies(Stream):
    name = "companies"
    key_properties = ["hs_object_id"]
    replication_method = "INCREMENTAL"
    replication_key = "hs_lastmodifieddate"

    def sync(self, state):
        LOGGER.info("%s: Starting sync", self.name)

        # Counter
        counter = metrics.Counter("record_count", {"endpoint": self.name})

        # Get the current bookmar
        current_bookmark = bookmark.get_bookmark(self, state)

        # Write in state variable
        singer.write_bookmark(
            state, self.name, self.replication_key, current_bookmark.isoformat()
        )

        all_companies = self.client.crm.companies.get_all()

        # console.log(str(len(all_companies)) + " companies", style="bold cyan")

        batch_properties = ["domain", "name", "type", "industry", "city", "country"]
        enriched_companies = enrich_data(
            self,
            current_bookmark,
            all_companies,
            batch_properties,
            self.client.crm.companies,
        )

        # console.log(str(len(enriched_companies)) + " enriched companies", style="bold cyan")

        # For each record, transform and log the data
        for company in enriched_companies:
            # Transformation of the data in order to select the right records and STOUT the singer message
            outcome = transform.transform_and_log(
                self, state, company.properties, self.replication_key, current_bookmark
            )
            if outcome:
                # Only count successful record transformations
                counter.increment()

        # Modify the state
        if self.replication_method == "INCREMENTAL":
            singer.write_state(state)

        LOGGER.info("%s: Completed sync (%s rows)", self.name, counter.value)


class Deals(Stream):
    name = "deals"
    key_properties = ["hs_object_id"]
    replication_method = "INCREMENTAL"
    replication_key = "hs_lastmodifieddate"

    def sync(self, state):
        LOGGER.info("%s: Starting sync", self.name)

        # Counter
        counter = metrics.Counter("record_count", {"endpoint": self.name})

        # Get the current bookmar
        current_bookmark = bookmark.get_bookmark(self, state)

        # Write in state variable
        singer.write_bookmark(
            state, self.name, self.replication_key, current_bookmark.isoformat()
        )

        # API Logic

        all_deals = self.client.crm.deals.get_all()

        # console.log(str(len(all_deals)) + " deals", style="bold cyan")

        batch_properties = [
            "amount",
            "closedate",
            "createdate",
            "dealname",
            "dealstage",
            "hs_lastmodifieddate",
            "hs_object_id",
            "pipeline",
            "hubspot_owner_id",
            "deal_currency_code",
        ]
        enriched_deals = enrich_data(
            self, current_bookmark, all_deals, batch_properties, self.client.crm.deals,
        )
        # console.log(str(len(enriched_deals)) + " enriched deals", style="bold cyan")

        associations_companies = enrich_data(
            self,
            current_bookmark,
            all_deals,
            batch_properties,
            self.client.crm.associations,
            "deals_companies",
        )

        associations_contacts = enrich_data(
            self,
            current_bookmark,
            all_deals,
            batch_properties,
            self.client.crm.associations,
            "deals_contacts",
        )

        deals = [deal.properties for deal in enriched_deals]

        for association in associations_companies:
            deal_id = str(association._from.id)
            companies_ids = list(map(lambda x: x.id, association.to))
            temp = find(deals, {"hs_object_id": deal_id})
            temp["associated_companies"] = companies_ids

        for association in associations_contacts:
            deal_id = str(association._from.id)
            contacts_ids = list(map(lambda x: x.id, association.to))
            temp = find(deals, {"hs_object_id": deal_id})
            temp["associated_contacts"] = contacts_ids

        # For each record, transform and log the data
        for deal in deals:
            # Transformation of the data in order to select the right records and STOUT the singer message
            outcome = transform.transform_and_log(
                self, state, deal, self.replication_key, current_bookmark
            )
            if outcome:
                # Only count successful record transformations
                counter.increment()

        # Modify the state
        if self.replication_method == "INCREMENTAL":
            singer.write_state(state)

        LOGGER.info("%s: Completed sync (%s rows)", self.name, counter.value)


STREAMS = {"contacts": Contacts, "companies": Companies, "deals": Deals}
