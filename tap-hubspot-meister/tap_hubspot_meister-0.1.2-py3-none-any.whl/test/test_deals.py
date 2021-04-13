import os

from hubspot import HubSpot
from hubspot.crm import ObjectType
from hubspot.crm.associations import BatchInputPublicObjectId
from hubspot.crm.contacts import (BatchReadInputSimplePublicObjectId,
                                  SimplePublicObjectId)
from pydash import find
from rich.console import Console

console = Console()
client = HubSpot()
tokens = client.auth.oauth.default_api.create_token(
    grant_type="refresh_token",
    redirect_uri="http://example.com",
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    refresh_token=os.environ["REFRESH_TOKEN"],
)
client.access_token = tokens.access_token
os.environ["REFRESH_TOKEN"] = tokens.refresh_token
inputs = [SimplePublicObjectId(id=deal.id) for deal in hubspot.crm.deals.get_all()]
properties = [
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
enriched_deals = hubspot.crm.deals.batch_api.read(
    batch_read_input_simple_public_object_id=BatchReadInputSimplePublicObjectId(
        inputs=inputs, properties=properties,
    )
)

associations_companies = hubspot.crm.associations.batch_api.read(
    ObjectType.DEALS,
    ObjectType.COMPANIES,
    batch_input_public_object_id=BatchInputPublicObjectId(inputs=inputs),
)
associations_contacts = hubspot.crm.associations.batch_api.read(
    ObjectType.DEALS,
    ObjectType.CONTACTS,
    batch_input_public_object_id=BatchInputPublicObjectId(inputs=inputs),
)

deals = [deal.properties for deal in enriched_deals.results]

for association in associations_companies.results:
    deal_id = str(association._from.id)
    companies_ids = list(map(lambda x: x.id, association.to))
    temp = find(deals, {"hs_object_id": deal_id})
    temp["associated_companies"] = companies_ids

for association in associations_contacts.results:
    deal_id = str(association._from.id)
    contacts_ids = list(map(lambda x: x.id, association.to))
    temp = find(deals, {"hs_object_id": deal_id})
    temp["associated_contacts"] = contacts_ids

console.log(deals)
