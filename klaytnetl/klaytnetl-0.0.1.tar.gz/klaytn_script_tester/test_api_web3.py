# %%
# Append parent package (DEV)
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from klaytnetl.cli import (
    get_block_range_for_timestamps,
    export_enrich_block_group
)
import os

# %%
from datetime import datetime, timezone

# %%
start_timestamp = datetime(2021, 4, 3, 0, tzinfo=timezone.utc).timestamp()
end_timestamp = datetime(2021, 4, 3, 1, tzinfo=timezone.utc).timestamp()
print(start_timestamp)
print(end_timestamp)

# %%
get_block_range_for_timestamps.callback(
    start_timestamp=int(start_timestamp),
    end_timestamp=int(end_timestamp),
    output='./temp/metadata/block_date=2021-04-03/block_hour=00/block-info.txt',
    provider_uri="http://35.188.61.188:8551",
    api_service='web3',
)

# 55707329,55710929
# 55754090,55757689
# 55757690,55761289
# 55761290,55764889
# 55764890,55768485
# 55768486,55772085



# %%
export_enrich_block_group.callback(
    start_block=55707329,
    end_block=55710929,
    batch_size=20,
    provider_uri="http://35.188.61.188:8551",
    max_workers=10,
    blocks_output="./temp/blocks/block_date=2021-04-03/block_hour=00",
    transactions_output="./temp/transactions/block_date=2021-04-03/block_hour=00",
    logs_output="./temp/logs/block_date=2021-04-03/block_hour=00",
    token_transfers_output="./temp/token_transfers/block_date=2021-04-03/block_hour=00",
    file_format="json",
    file_maxlines=1000,
    compress=False,
    api_service='web3',
)
# %%
