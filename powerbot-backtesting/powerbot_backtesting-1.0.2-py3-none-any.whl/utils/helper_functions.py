import os
from typing import List, Dict
from datetime import datetime
from decimal import Decimal, getcontext
from pathlib import Path
import pandas as pd

from PowerbotBacktesting.utils import *

def _cache_data(data_type: str,
                data: Dict[str, pd.DataFrame],
                delivery_area: str,
                exchange: str = None,
                api_client: object = None,
                gzip_files: bool = True,
                as_csv: bool = False):
    """
    Function to be called by data request functions to cache loaded data in a reusable format. Automatically generates
    a folder to cache loaded files, if it cannot find an existing one.

    Args:
        data_type (str): trade or order
        data (dict): Dictionary of DataFrames
        delivery_area (str): EIC Area Code for Delivery Area
        exchange (str): Exchange e.g. epex, nordpool, southpool, etc.
        api_client: PowerBot ApiClient
        gzip_files (bool): True if cached files should be gzipped
        as_csv (bool): if True, will save files as CSV, additionally to JSON
    """
    # Setup
    host = api_client.configuration.host if api_client else None
    environment = "staging" if host and host.split("/")[2].split(".")[0] == "staging" else "prod"
    exchange = host.split("/")[4] if host else exchange
    data_types = {"trade": "trades", "order": "ordhist"}
    compression = "gzip" if gzip_files else "infer"
    file_ending = ".gz" if gzip_files else ""

    # Caching
    for key, value in data.items():
        delivery_date = datetime.strptime(key.split(" ")[0], "%Y-%m-%d")
        year_month = delivery_date.strftime("%Y-%m")
        day_month = delivery_date.strftime("%m-%d")
        file_name = key.replace(f"{str(key).split(' ')[0]}", "").replace(":", "-")

        # Check if __cache__ already exists
        cache_path = _find_cache()

        # Assure That Directory Exists
        cache_path.joinpath(f"{environment}\\{exchange}_{delivery_area}\\{year_month}\\{day_month}\\{'raw'}").mkdir(
            parents=True, exist_ok=True)

        # Cache File If It Doesn't Exist Yet
        if not cache_path.joinpath(
                f"{environment}\\{exchange}_{delivery_area}\\{year_month}\\{day_month}\\"
                f"{'raw'}\\{file_name}_{data_types[data_type]}.json{file_ending}").exists():
            value.to_json(cache_path.joinpath(
                f"{environment}\\{exchange}_{delivery_area}\\{year_month}\\{day_month}\\{'raw'}\\"
                f"{file_name}_{data_types[data_type]}.json{file_ending}"),
                date_format="iso", date_unit="us", compression=compression)

        if as_csv:
            value.to_csv(cache_path.joinpath(
                f"{environment}\\{exchange}_{delivery_area}\\{year_month}\\{day_month}\\"
                f"{'raw'}\\{file_name}_{data_types[data_type]}.csv{file_ending}"),
                sep=";", compression=compression)


def _find_cache():
    """
    Functions returns location of __cache__ directory if it can be found within 3 parent directories based on the
    location of the file backtesting functions are called from. It is assumed that the swagger_client that is necessary
    for this package is located directly under the project root, therefore the function will stop once it finds this
    directory. Cache will not be created outside of project directory.

    Returns:
        Path
    """
    if Path("__pb_cache__").exists():
        return Path("__pb_cache__")

    cache_path = None
    root_path = Path().cwd()

    for _ in range(3):
        cache_path = [root for root, directory, file in os.walk(root_path) if "__pb_cache__" in root]

        # Check if cache was found
        if cache_path:
            cache_path = Path(cache_path[0])
            break

        # Check if project root was reached
        if "swagger_client" in [x for i in [directory for root, directory, file in os.walk(root_path)] for x in i]:
            break

        root_path = root_path.parent


    if not cache_path:
        cache_path = Path().cwd().joinpath("__pb_cache__")

    return cache_path


def _get_file_cachepath(api_client, contract_key, delivery_area):
    """
    Helper function that constructs most of the path of a cached file.

    Args:
        api_client: ApiClient
        contract_key: Key of dictionary

    Returns:
        filepath: str
    """
    environment = api_client.configuration.host.split("/")[2].split(".")[0]
    market = api_client.configuration.host.split("/")[4]
    delivery_date = datetime.strptime(contract_key.split(" ")[0], DATE_YMD)
    year_month = delivery_date.strftime(DATE_YM)
    day_month = delivery_date.strftime(DATE_MD)
    file_name = contract_key.replace(f"{str(contract_key).split(' ')[0]}", "").replace(":", "-")

    return f"{environment}\\{market}_{delivery_area}\\{year_month}\\{day_month}\\raw\\{file_name}"


def _check_contracts(contract, delivery_areas: List[str], products: List[str]):
    """
    Helper function to determine if contract is of interest and should be added to contract dictionary.

    Args:
        contract: Contract Object
        delivery_areas: List of EIC-codes
        products: List of products

    Returns:
        Bool
    """
    if delivery_areas and contract.delivery_areas and not any(area in contract.delivery_areas for area in delivery_areas)\
            or delivery_areas and contract.contract_details["deliveryAreas"] and not any(area in contract.contract_details["deliveryAreas"] for area in delivery_areas)\
            or delivery_areas and not contract.delivery_areas and not contract.contract_details["deliveryAreas"]\
            or products and not contract.product in products\
            or not products and "10YGB----------A" not in delivery_areas and contract.product == "GB_Hour_Power":
        return False
    return True


def _order_matching(order_side: str,
                    orderbook: pd.DataFrame,
                    timestamp: str,
                    price: int,
                    quantity: int,
                    exec_orders_list: Dict[str, int],
                    trade_list: Dict[int, Dict[str, int]],
                    contract_time: datetime) -> int:
    """
    Matches orders according to input parameters; add trades made to trade_list and returns the remaining quantity.

    Args:
        order_side (str): buy/sell
        orderbook (DataFrame): Single Orderbook
        timestamp(str): Timestamp of Orderbook
        price (int): Minimum/ Maxmimum Price for Transaction
        quantity (int): Quantity to buy/sell
        exec_orders_list (dict): Dictionary of already matched order IDs
        trade_list (list): List of executed trades
        contract_time (datetime):

    Returns:
        quantity: remaining quantity as int
    """

    # Transform Values to Decimals
    getcontext().prec = 6
    price = round(Decimal(price), 2)
    quantity = round(Decimal(quantity), 1)
    cash_adjust = {60: 1, 30: 2, 15: 4}

    order_type = {"buy": "ask", "sell": "bid"}
    operator = {"buy": -1, "sell": 1}

    orderbook = orderbook[orderbook.type == order_type[order_side]]

    if order_type[order_side] == "ask":
        orderbook = orderbook.sort_values(by=['price', 'as_of'], ascending=[True, False])
    else:
        orderbook = orderbook.sort_values(by=['price', 'as_of'], ascending=[False, False])

    for ind, row in orderbook.iterrows():
        if quantity > 0:
            open_qty = round(Decimal(row["quantity"]), 1)

            if row["order_id"] in [*exec_orders_list]:  # Check If Already Matched
                if round(Decimal(exec_orders_list[row["order_id"]]), 1) == open_qty:
                    continue  # Skip If Quantity Depleted
                open_qty = open_qty - Decimal(exec_orders_list[row["order_id"]])  # If Matched, Adjust Open Quantity

            # Check If Price Is Matched
            price_match = Decimal(row["price"]) <= price if order_side == "buy" else Decimal(row["price"]) >= price

            if price_match:
                traded_quant = round(min(open_qty, quantity), 1)
                cash = round(traded_quant * Decimal(row.price) * operator[order_side] / cash_adjust[contract_time],
                             2)  # Calculate Cost

                trade_list[len([*trade_list]) + 1] = {"Side": order_side,
                                                      "Quantity": float(str(traded_quant)),
                                                      "Price": row["price"],
                                                      "Cash": float(str(cash)),
                                                      "Timestamp": timestamp}

                if row["order_id"] in [*exec_orders_list]:
                    # If Existing, Adjust Quantity
                    if order_side == "buy":
                        exec_orders_list[row["order_id"]] += round(min(open_qty, quantity), 1)
                    else:
                        exec_orders_list[row["order_id"]] -= round(min(open_qty, quantity), 1)
                else:
                    exec_orders_list[row["order_id"]] = round(min(open_qty, quantity), 1)

                quantity -= round(traded_quant, 1)  # Adjust Quantity
            else:
                break
        else:
            break

    return quantity

def _orderbook_data_transformation(orders: pd.DataFrame):
    '''
    Function transforms data in passes dataframe to be compatible with process_orderbooks function

    Returns:
        Dataframe
    '''
    if not isinstance(orders, pd.DataFrame):
        return pd.DataFrame()

    bids_asks = []
    # Processing
    if "orders" in orders.columns:
        orders_all = orders["orders"].to_list()
        dates_all = [str(i) for i in orders["as_of"].to_list()]
        for nr, val in enumerate(orders_all):
            for k, v in val.items():
                if v:
                    if k == "bid":
                        for x in v:
                            x["as_of"] = dates_all[nr]
                            x["type"] = "bid"
                            bids_asks.append(x)
                    if k == "ask":
                        for x in v:
                            x["as_of"] = dates_all[nr]
                            x["type"] = "ask"
                            bids_asks.append(x)

    else:
        for nr, row in orders.iterrows():
            for side in ["bids", "asks"]:
                if row[side]:
                    for entry in row[side]:
                        entry["type"] = side
                        entry["as_of"] = row["as_of"]
                        bids_asks.append(entry)

    df_bid_asks = pd.DataFrame(bids_asks)
    df_bid_asks = df_bid_asks.drop(columns=["exe_restriction", "delivery_area", "order_entry_time"],
                                   errors="ignore")
    return df_bid_asks



def _historic_data_transformation(files, exchange, filetype):
    df = None
    for file in files:
        if not isinstance(df, pd.DataFrame):
            df = pd.read_json(file)
        else:
            df = df.append(pd.read_json(file), ignore_index=True)

    if exchange != "nordpool":
        if filetype == "trades":
            df.drop(columns=["revisionNo"], inplace=True)
            df.rename(columns={"_id": "trade_id", "contractId": 'contract_id', "tradeExecTime": 'exec_time',
                               "apiTimeStamp": 'api_timestamp', "buyDeliveryArea": 'buy_delivery_area',
                               "sellDeliveryArea": 'sell_delivery_area', "selfTrade": 'self_trade',
                               "qty": 'quantity',"px": 'price', "pxqty": 'prc_x_qty'},
                      inplace=True)

            df.quantity = df.quantity / 100
            df.price = df.price / 100
            df.prc_x_qty = df.prc_x_qty / 100

        if filetype == "orders":
            df.rename(columns={"asOf": "as_of", "bestAskPrice": "best_ask", "bestAskQuantity": "best_ask_qty",
                               "bestBidPrice": "best_bid", "bestBidQuantity": "best_bid_qty",
                               "contractId": "contract_id", "deliveryArea": "delivery_area", "full": "delta",
                               "lastPrice": "last_price", "lastQuantity": "last_qty",
                               "lastUpdate": "last_trade_time", "revisionNo": "revision_no"},
                      inplace=True)

            # Getting information from details field if missing on upper level
            meta_cols = {"best_bid": "bestBidPx", "best_ask": "bestAskPx", "best_bid_qty": "bestBidQty",
                         "last_price": "lastPx", "last_qty": "lastQty", "last_trade_time": "lastTradeTime",
                         "volume": "totalQty", "high": "highPx", "low": "lowPx"}
            missing_details = {k: v for k, v in meta_cols.items() if k not in df.columns}
            details = df.details.tolist()

            for k, v in missing_details.items():
                if v in ["lastPx", "lastQty", "highPx", "lowPx", "totalQty"]:
                    df[k] = [i[v] / 100 if v in [*i] else None for i in details]
                else:
                    df[k] = [i[v] if v in [*i] else None for i in details]

            contract_id = df.contract_id.unique().tolist()[0]
            delivery_area = df.delivery_area.unique().tolist()[0]
            asks = [i["sellOrdrList"]["ordrBookEntry"] if i["sellOrdrList"] else None for i in df.details.tolist()]
            bids = [i["buyOrdrList"]["ordrBookEntry"] if i["buyOrdrList"] else None for i in df.details.tolist()]

            conversion = lambda i: [{"order_id": v["ordrId"], "price": v["px"] / 100, "quantity": v["qty"] / 100,
                                     "contract_id": contract_id, "delivery_area": delivery_area,
                                     "order_entry_time": v["ordrEntryTime"]} for v in i]

            asks = [conversion(i) if i else None for i in asks]
            bids = [conversion(i) if i else None for i in bids]

            df["asks"] = asks
            df["bids"] = bids

            df.drop(columns=["_id", "details", "avwa", "bvwa"], inplace=True, errors="ignore")

    else:
        if filetype == "trades":
            # Filter out deleted Trades
            df = df[df.deleted != True]

            df.rename(columns={"_id": "trade_id", "tradeTime": 'exec_time', "apiTimestamp": "api_timestamp",
                               "companyTrade": "self_trade"},
                      inplace=True)

            details = df.legs.tolist()

            df["contract_id"] = [i[0]["contractId"] for i in details]
            df["buy_delivery_area"] = [self.NORDPOOL_EIC_CODES[i[0]["deliveryAreaId"]] if i else None for i in
                                       details]
            df["sell_delivery_area"] = [self.NORDPOOL_EIC_CODES[i[1]["deliveryAreaId"]] if len(i) == 2 else None for
                                        i in
                                        details]
            df["quantity"] = [float(i[0]["quantity"]) for i in details]
            df["price"] = [float(i[0]["unitPrice"]) for i in details]
            df["prc_x_qty"] = round(df.price * df.quantity, 2)

            df.drop(columns=["eventSequenceNo", "legs", "mediumDisplayName", "deleted", "state"], inplace=True)

        if filetype == "orders":
            df.rename(
                columns={"apiTimestamp": "as_of", "bestAskPrice": "best_ask", "bestAskQuantity": "best_ask_qty",
                         "bestBidPrice": "best_bid", "bestBidQuantity": "best_bid_qty", "bidsAndAsks": "details",
                         "contractId": "contract_id", "deliveryArea": "delivery_area", "full": "delta",
                         "lastPrice": "last_price", "lastQuantity": "last_qty", "lowestPrice": "low",
                         "highestPrice": "high", "lastTradeTime": "last_trade_time", "revision": "revision_no",
                         "turnover": "total_quantity"},
                inplace=True)

            df.revision_no = [i for i in range(0, len(df))]
            df.delivery_area = [self.NORDPOOL_EIC_CODES[i] for i in df.delivery_area.tolist()]
            asks = [i["asks"] if "asks" in i else None for i in df.details.tolist()]
            bids = [i["bids"] if "bids" in i else None for i in df.details.tolist()]

            conversion = lambda i: [
                {"order_id": v["orderId"], "price": v["price"], "quantity": v["quantity"],
                 "contract_id": v["contractId"], "delivery_area": self.NORDPOOL_EIC_CODES[v["deliveryArea"]],
                 "order_entry_time": v["createdAt"]} for v in i]

            df["asks"] = [conversion(i) if i else None for i in asks]
            df["bids"] = [conversion(i) if i else None for i in bids]

            df.drop(columns=["_id", "details", "updatedAt"], inplace=True)

    return df