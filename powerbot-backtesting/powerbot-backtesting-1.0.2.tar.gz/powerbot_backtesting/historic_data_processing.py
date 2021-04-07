import os
import shutil
from pathlib import Path
from datetime import timedelta
import pandas as pd
from typing import List

from PowerbotBacktesting.utils.constants import *
from PowerbotBacktesting.utils import _cache_data,_find_cache, _historic_data_transformation

def process_historic_data(extracted_files: List[str], exchange: str):
    """
    Function processes list of files extracted from a zip-file downloaded via History API to be compatible with the
    rest of the PowerbotBacktesting package. Once files have been processed, they are cached in the same manner as
    data loaded via PowerBot API, allowing functions like get_contract_history and get_public_trades to load them from
    the cache.

    Args:
        extracted_files List(str): List of files extracted with get_historic_data (-> return value of get_historic_data)
        exchange (str): One of the following: epex, hupx, tge, nordpool, southpool
    """
    for filename, unzipped_files in extracted_files.items():
        contract_file = [i for i in unzipped_files if "contracts.json" in i][0]
        contract_file = unzipped_files.pop(unzipped_files.index(contract_file))

        delivery_area = filename.split("_")[0]

        # Group contracts after delivery period
        df = pd.read_json(contract_file)

        df['deliveryStart'] = pd.to_datetime(df['deliveryStart'])
        df['deliveryEnd'] = pd.to_datetime(df['deliveryEnd'])

        df.sort_values(by=["deliveryStart"], inplace=True)

        contract_times = {}
        start = df.deliveryStart.iloc[0]
        end = df.deliveryStart.iloc[-1]

        while start <= end:
            for timestep in [15, 30, 60]:
                ids = df[(df.deliveryStart==start)&(df.deliveryEnd==(start+timedelta(minutes=timestep)))]._id.tolist()
                if ids:
                    contract_times[f"{start.strftime(DATE_YMD_TIME_HM)} - {(start+timedelta(minutes=timestep)).strftime(TIME_HM)}"] = ids
            start += timedelta(minutes=15)

        transformed_trade_files, transformed_order_files = {}, {}

        # For each timestep
        for time, ids in contract_times.items():
            files = {}
            files["trades"] = [i for i in unzipped_files if any(str(x) in i for x in ids) and "Trades" in i]
            files["orders"] = [i for i in unzipped_files if any(str(x) in i for x in ids) and "Orders" in i]

            for k, v in files.items():
                if v:
                    if k == "trades":
                        transformed_trade_files[time] = _historic_data_transformation(v, exchange, k)
                    else:
                        transformed_order_files[time] = _historic_data_transformation(v, exchange, k)

        # Cache the result
        _cache_data("trade", transformed_trade_files, delivery_area, exchange)
        _cache_data("order", transformed_order_files, delivery_area, exchange)

        # Cleanup
        for file in unzipped_files:
            Path(file).unlink(missing_ok=True)
        Path(contract_file).unlink(missing_ok=True)

    # Delete history directory if it's empty (no files)
    history_path = _find_cache().joinpath("history")
    history_files = [file for root, directory, file in os.walk(history_path)]

    if not all(i for i in history_files):
        shutil.rmtree(history_path)