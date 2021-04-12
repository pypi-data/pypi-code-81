import os

from hubspot import HubSpot

api_client = HubSpot()
tokens = api_client.auth.oauth.default_api.create_token(
    grant_type="refresh_token",
    redirect_uri="http://example.com",
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    refresh_token=os.environ["REFRESH_TOKEN"],
)
api_client.access_token = tokens.access_token
os.environ["REFRESH_TOKEN"] = tokens.refresh_token
# api_client.access_token = "your_access_token"
