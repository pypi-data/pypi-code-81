# %%
import requests
import json

# %%[markdown]
# ### Test addresses
# - 0xf86c03a92a076137c5cb258994f26e2a582acf6b
# - 0xd307d6a43afa6635427358b3c21bfc095cbb1bf6
# - 0x3391bc19932524d3f932ce3b7699cba033f540ef
# - 0x698b5b9e6d1e2df4cf501021335cc8369826e60e
# - 0xc2b4d3ebd2ab9f89dc2e199364657f0a8c787999
# - 0x898f2afc07924f5a4f9612449e4c4f8eca527515
# - 0x2f5dc7dce80d30c122999087f41059d40bc94c52
# - 0x113d6148e2ee1382a4c34bfe89e4ae1eac5c1220
# - 0x48c9abff72c070b8d2e91ae9d8eede348eeec06c
# - 0xf55bad6cf6891299072a8c9d0a00992749ccc8de
# - 0x50399447ce7ea0e94cce10cf0ca60b3f92aa9448
# - 0xa11fb48df81714ac4ea11e8448a0b15410057150
# - 0x6d262df831c52941cb2752615c2fea79b21f656f
# - 0x7273b642bc28a31724899b5d6cda4fdbeba34ffe
# - 0x08c3c2d9e3738c243d402f6d04e6a351a9f0f6de
# - 0xcebbef2d1d6cb7f9f18039ed09195c57d3e3a75d
# - 0xb879a6b9b91d6ddb637f8b28ea845f9c59931b97
# - 0x53571b1eb0c1bed4e06be67e78a1977cc0bd9b74

# %%
resp = requests.get("https://th-api.klaytnapi.com/v2/transfer", params=dict(
    range="",
    size=1000,
    presets=133
), headers={
    "ContentType": "application/json",
    "x-chain-id": "8217"
}, auth=('KASKKB3WG1PRS40GTWPY54QZ', 'kwmEkAKbQp8sRJ6N2OxPHJcrVoGr8TgTQaTh4sPv'))

# %%
result = json.loads(resp.text)

# %%
result

# %%
with open('./token_info.jsonl', 'w+') as fp:
    for row in result['items']:
        fp.write(json.dumps(row) + "\n")

# %%
token_transfers = []
with open('./token_info.jsonl', 'r+') as fp:
    for line in fp:
        token_transfers.append(json.loads(line))
# %%
token_transfers

# %%
token_transfers
# %%
import pandas as pd
import numpy as np


# %%
for tt in token_transfers:
    for k, v in tt['transaction'].items():
        tt[f'transaction_{k}'] = v
    for k, v in tt['contract'].items():
        tt[f'contract_{k}'] = v
    tt['transaction'] = None
    tt['contract'] = None
# %%
tt
# %%
# %%
df = pd.DataFrame(token_transfers)
df

# %%
tss = df['transaction_timestamp'].to_list()

# %%
from datetime import datetime, timedelta
dts = [datetime.utcfromtimestamp(ts) for ts in tss]
# %%
dts

# %%
df['dt'] = pd.to_datetime(df['transaction_timestamp'], unit='s')
# %%
df
# %%
df['date'] = df['dt'].dt.date
df['hour'] = df['dt'].dt.hour
# %%
df.groupby(['date', 'hour']).nunique()
# %%
df
# %%



# %%
from web3 import Web3
from web3.middleware import geth_poa_middleware
import requests
import json

# %%
w3 = Web3(Web3.HTTPProvider("https://rpc-mainnet.maticvigil.com/v1/927c67086ea722f1b98b3ec14b174ce140d3a84e"))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

# %%
block = w3.eth.getBlock("0x123123")

# %%
block

# %%
resp = requests.post("https://node-api.klaytnapi.com/v1/klaytn", json={
    "id": 1,
    "jsonrpc": "2.0",
    "method": "klay_getBlockWithConsensusInfoByNumber",
    "params": ['latest']
}, headers={
    "ContentType": "application/json",
    "x-chain-id": "8217"
}, auth=('KASKKB3WG1PRS40GTWPY54QZ', 'kwmEkAKbQp8sRJ6N2OxPHJcrVoGr8TgTQaTh4sPv'))
# %%
block_data = json.loads(resp.text)
# %%
resp.text
# %%
block_data.keys()

# %%
# %%
# Append parent package (DEV)
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# %%
import json

# %%
from klaytnetl.providers.rpc import KasBatchHTTPProvider
from klaytnetl.json_rpc_requests import generate_get_block_with_receipt_by_number_json_rpc

# %%
provider = KasBatchHTTPProvider(
    endpoint_uri="https://node-api.klaytnapi.com/v1/klaytn",
    request_kwargs={
        "headers" : {
            "ContentType": "application/json",
            "x-chain-id": "8217"
        },
        "auth": ('KASKKB3WG1PRS40GTWPY54QZ', 'kwmEkAKbQp8sRJ6N2OxPHJcrVoGr8TgTQaTh4sPv'),
    })

# %%
block_number_batch = [0x3556db1, 0x3556db2]
blocks_rpc = list(generate_get_block_with_receipt_by_number_json_rpc(block_number_batch))
blocks_rpc

# %%
resp = provider.make_batch_request(
    blocks_rpc
)

# %%
resp = provider.make_request(
    method='klay_getBlockWithConsensusInfoByNumber',
    params=['0x3556db1'],
)

# %%
resp

# %%
resp = requests.post("https://node-api.klaytnapi.com/v1/klaytn", json=[{
    "id": 1,
    "jsonrpc": "2.0",
    "method": "klay_getBlockWithConsensusInfoByNumber",
    "params": [0x3556db1]
}, {
    "id": 2,
    "jsonrpc": "2.0",
    "method": "klay_getBlockWithConsensusInfoByNumber",
    "params": [0x3556db2]
}], headers={
    "ContentType": "application/json",
    "x-chain-id": "8217"
}, auth=('KASKKB3WG1PRS40GTWPY54QZ', 'kwmEkAKbQp8sRJ6N2OxPHJcrVoGr8TgTQaTh4sPv'))

# %%
resp

# %%
resp = requests.post("https://node-api.klaytnapi.com/v1/klaytn", json={
    "id": 1,
    "jsonrpc": "2.0",
    "method": "klay_getBlockWithConsensusInfoByNumber",
    "params": ["0x3556db1"]
}, headers={
    "ContentType": "application/json",
    "x-chain-id": "8217"
}, auth=('KASKKB3WG1PRS40GTWPY54QZ', 'kwmEkAKbQp8sRJ6N2OxPHJcrVoGr8TgTQaTh4sPv'))

# %%
resp.text


# %%
# Append parent package (DEV)
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from ethereumetl.cli import (
    get_klay_block_range_for_timestamps,
    export_enrich_block_group
)
import os

# %%
from datetime import datetime, timezone

# %%
start_timestamp = datetime(2021, 4, 3, 17, tzinfo=timezone.utc).timestamp()
end_timestamp = datetime(2021, 4, 3, 18, tzinfo=timezone.utc).timestamp()
print(start_timestamp)
print(end_timestamp)

# %%
get_klay_block_range_for_timestamps.callback(
    start_timestamp=int(start_timestamp),
    end_timestamp=int(end_timestamp),
    output='./temp/metadata/block_date=2021-04-03/block_hour=17/block-info.txt',
    provider_uri="https://node-api.klaytnapi.com/v1/klaytn",
    api_service='kas',
    auth_id='KASKKB3WG1PRS40GTWPY54QZ',
    auth_secret='kwmEkAKbQp8sRJ6N2OxPHJcrVoGr8TgTQaTh4sPv',
    x_chain_id='8217'
)

# 55707329,55710929
# 55754090,55757689
# 55757690,55761289
# 55761290,55764889
# 55764890,55768485
# 55768486,55772085



# %%
export_enrich_block_group.callback(
    start_block=55768486,
    end_block=55772085,
    batch_size=1,
    provider_uri="https://node-api.klaytnapi.com/v1/klaytn",
    max_workers=15,
    blocks_output="./temp/blocks/block_date=2021-04-03/block_hour=17",
    transactions_output="./temp/transactions/block_date=2021-04-03/block_hour=17",
    logs_output="./temp/logs/block_date=2021-04-03/block_hour=17",
    token_transfers_output="./temp/token_transfers/block_date=2021-04-03/block_hour=17",
    file_format="json",
    file_maxlines=1000,
    compress=False,
    api_service='kas',
    auth_id='KASKKB3WG1PRS40GTWPY54QZ',
    auth_secret='kwmEkAKbQp8sRJ6N2OxPHJcrVoGr8TgTQaTh4sPv',
    x_chain_id='8217'
)
# %%
