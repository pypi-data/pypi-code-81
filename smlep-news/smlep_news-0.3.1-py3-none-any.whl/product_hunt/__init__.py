import requests

from .product import Product


base = "https://api.producthunt.com/v2"


def get_access_token(client_id, client_secret):
    url = "{}/oauth/token".format(base)
    r = requests.post(
        url,
        json={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        },
    )
    r.raise_for_status()
    return r.json()["access_token"]


def get_top_products(client_id, client_secret, from_date, count=10):
    token = get_access_token(client_id, client_secret)
    url = base + "/api/graphql"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        "Host": "api.producthunt.com",
    }
    # .format() does not handles well {} in strings, falling back to %s
    body = {
        "query": 'query { posts( first: %s postedAfter: "%s" order: VOTES) {   edges {    node {  id  name description tagline url votesCount }  } } } '
        % (count, from_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z"))
    }

    r = requests.post(url, json=body, headers=headers)
    r.raise_for_status()
    return [Product(p["node"]) for p in r.json()["data"]["posts"]["edges"]]
