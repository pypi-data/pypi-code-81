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
