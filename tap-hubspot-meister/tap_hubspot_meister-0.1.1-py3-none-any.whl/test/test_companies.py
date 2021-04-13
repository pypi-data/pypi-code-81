import os

from hubspot import HubSpot
from hubspot.crm.contacts import (BatchReadInputSimplePublicObjectId,
                                  SimplePublicObjectId)
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
inputs = [
    SimplePublicObjectId(id=company.id) for company in hubspot.crm.companies.get_all()
]
enriched_companies = hubspot.crm.companies.batch_api.read(
    batch_read_input_simple_public_object_id=BatchReadInputSimplePublicObjectId(
        inputs=inputs,
        properties=["domain", "name", "type", "industry", "city", "country"],
    )
)

for element in enriched_companies.results:
    console.log(element.properties)
