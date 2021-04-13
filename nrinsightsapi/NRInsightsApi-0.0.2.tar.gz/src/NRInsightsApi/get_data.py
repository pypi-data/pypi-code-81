import requests
import json
import pandas as pd
import gzip

def get_data(account,query_api_key,query):
    url = f'https://insights-api.newrelic.com/v1/accounts/{account}/query'
    params= {'nrql':query}

    headers = { "Accept": "application/json",'X-Query-Key': query_api_key}
    get_request = requests.get(url, headers=headers, params=params)
    result_json = get_request.json()
    return result_json



