import requests
import json
import pandas as pd
import gzip


def insert_data(account,insert_api_key,data_df):
    url = f'https://insights-collector.newrelic.com/v1/accounts/{account}/events'
    headers = { "Content-Type": "application/json",'X-Insert-Key': insert_api_key}
    
    start = 0
    end = 2500
    offset = 2500
    response_data = []
    loops = len(data_df.index)//2500 + 2
    for r in range(0,loops):
        reduced_df = data_df.iloc[start:end:]
        start += offset
        end +=offset
        
        payload = reduced_df.to_dict('records')
        json_str = json.dumps(payload)
        json_bytes = gzip.compress(json_str.encode('utf-8'))
        
        post_request = requests.post(url, data =json_bytes, headers=headers)
        print(post_request)
        response_data.append(post_request)
    return response_data
    
    

