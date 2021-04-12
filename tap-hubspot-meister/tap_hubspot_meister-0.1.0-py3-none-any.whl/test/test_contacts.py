import os

from hubspot import HubSpot
from hubspot.crm.contacts import (
    BatchReadInputSimplePublicObjectId,
    SimplePublicObjectId,
)
from rich.console import Console
from singer import utils
import datetime


console = Console()
client = HubSpot()


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


tokens = client.auth.oauth.default_api.create_token(
    grant_type="refresh_token",
    redirect_uri="http://example.com",
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    refresh_token=os.environ["REFRESH_TOKEN"],
)


client.access_token = tokens.access_token
os.environ["REFRESH_TOKEN"] = tokens.refresh_token
contacts = client.crm.companies.get_all()
for contact in contacts:
    # The strptime is deprecated and the UTC version cannot be compated with a standard datetime
    # So it's importante to remove the tzinfo
    create_date = utils.strptime_to_utc(contact.properties["createdate"]).replace(
        tzinfo=None
    )
    if create_date > datetime.datetime(2021, 4, 5):
        console.log(create_date)

test = chunks(contacts, 100)
i = 1
for chunk in test:
    console.log(i, style="bold red")
    console.log(len(chunk))
    i += 1
"""



inputs = [
    SimplePublicObjectId(id=contact.id) for contact in client.crm.contacts.get_all()
]
enriched_contacts = client.crm.contacts.batch_api.read(
    batch_read_input_simple_public_object_id=BatchReadInputSimplePublicObjectId(
        inputs=inputs,
        properties=[
            "firstname",
            "lastname",
            "email",
            "associatedcompanyid",
            "hubspot_owner_id",
            "lifecyclestage",
            "jobtitle",
        ],
    )
)

for element in enriched_contacts.results:
    console.log(element.properties)
 """

