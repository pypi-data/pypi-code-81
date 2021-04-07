import json
import requests
from datetime import datetime, timedelta
from time import sleep
import pandas as pd
from typing import Dict, List
from dateutil.tz import tzutc
from collections import defaultdict

from powerbot_backtesting.utils.constants import *
from powerbot_backtesting.utils import  _cache_data, _check_contracts, \
    _get_file_cachepath, _find_cache

try:
    from swagger_client import Configuration, ApiClient, ContractApi, TradesApi, SignalsApi, Signal, Trade, \
        InternalTrade, OrdersApi, OwnOrder
    from swagger_client.rest import ApiException
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "You need an up-to-date swagger client in the top level of your project directory to run this package!")


def init_client(api_key: str, host: str) -> object:
    """
    Initializes PowerBot Client to enable data requests by the API.

    Args:
        api_key (str): API Key for PowerBot
        host (str): Host URL for PowerBot

    Returns:
        PowerBot ApiClient Object
    """
    config = Configuration()
    config.api_key['api_key'] = api_key
    config.host = host

    return ApiClient(config)


def get_contract_ids(api_client: ApiClient,
                     time_from: datetime = None,
                     time_till: datetime = None,
                     contract_ids: List[str] = None,
                     contract_time: str = "all",
                     products: List[str] = None,
                     delivery_areas: List[str] = None,
                     return_contract_objects: bool = False) -> Dict[str, List[str]]:
    """
    Loads all contract IDs for specified timeframe, either by hours, single day or multiple days. Alternatively, a list
    of contract IDs can be passed instead of a timeframe, returning a dictionary of contract IDs compatible with all other
    functions of the Backtesting package. If return_contract_objects is True, a dictionary of contract objects will be
    returned as well.

    If time_from includes hh:mm:ss
        loads data between both times in timesteps according to contract_time

    If time_from doesn't include hh:mm:ss
        loads data between both dates in timesteps according to contract_time

    Args:
        api_client: PowerBot ApiClient
        time_from (str/ datetime): yyyy-mm-dd or yyyy-mm-dd hh:mm:ss
        time_till (str/ datetime): yyyy-mm-dd or yyyy-mm-dd hh:mm:ss
        contract_ids (List[str]): Optionally, a list of specific contract IDs can be passed to return contract objects
        contract_time (str): all, hourly, half-hourly or quarter-hourly (all includes UDC)
        products (list): Optional list of specific products to return
        delivery_areas (list):
        return_contract_objects (bool): If True, returns complete Contract object

    Returns:
        Dict{key: (List[str])}: Dictionary of Contract IDs
        (Optional) Contract: Contract Object
    """
    # Check date input
    timeframes = {"all": 15, "hourly": 60, "half-hourly": 30, "quarter-hourly": 15}
    contract_api = ContractApi(api_client)
    products = [] if not products else products
    delivery_areas = [] if not delivery_areas else delivery_areas

    if not contract_ids:
        if not time_from and time_till:
            raise TypeError("If no specific contract IDs are given, a time period has to be defined.")

        if isinstance(time_from, str):
            try:
                if ":" in time_from:
                    time_from = datetime.strptime(time_from, DATE_YMD_TIME_HMS)
                    time_till = datetime.strptime(time_till, DATE_YMD_TIME_HMS)
                else:
                    time_from += " 00:00:00"
                    time_till += " 00:00:00"
                    time_from = datetime.strptime(time_from, DATE_YMD_TIME_HMS)
                    time_till = datetime.strptime(time_till, DATE_YMD_TIME_HMS)
            except (ValueError, TypeError):
                raise ValueError("Please use correct format: yyyy-mm-dd or yyyy-mm-dd hh:mm:ss")
    # Load Contract IDs
    contracts = defaultdict(list)

    # Loading by time_from & time_till
    if not contract_ids:
        while time_from != time_till:
            if contract_time != "all":
                new_contracts = contract_api.find_contracts(delivery_start=time_from,
                                                            delivery_end=time_from + timedelta(minutes=timeframes[contract_time]))
            else:
                new_contracts = contract_api.find_contracts(delivery_start=time_from)

            for c in new_contracts:
                # Check validity and add to contracts
                if _check_contracts(c, delivery_areas, products):
                    contracts[f"{time_from.strftime(DATE_YMD_TIME_HM)} - {c.delivery_end.strftime(TIME_HM)}"].append(c)

            time_from += timedelta(minutes=timeframes[contract_time])

    # Loading by specific contract IDs
    else:
        new_contracts = contract_api.find_contracts(contract_id=contract_ids)
        for c in new_contracts:
            # Check validity and add to contracts
            if _check_contracts(c, delivery_areas, products):
                # Add to contracts
                contracts[
                    f"{c.delivery_start.strftime(DATE_YMD_TIME_HM)} - {c.delivery_end.strftime(DATE_YMD_TIME_HM)}"] \
                    .append(c)

    # Cleanup
    contracts = {k: v for k, v in contracts.items() if v}
    contract_ids = {k: [c.contract_id for c in v] for k, v in contracts.items() if v}
    if not contracts:
        print("There was no contract data for your request!")

    # Returns Contract IDs and Object As A Whole
    if return_contract_objects:
        return contract_ids, contracts

    return contract_ids


def get_public_trades(api_client: ApiClient,
                      contract_ids: Dict[str, List[str]],
                      delivery_area: str,
                      contract_time: str,
                      iteration_delay: float = 0.4,
                      serialize_data: bool = True,
                      add_vwap: bool = False,
                      use_cached_data: bool = True,
                      caching: bool = True,
                      gzip_files: bool = True,
                      as_csv: bool = False) -> Dict[str, pd.DataFrame]:
    """
    Load trade data for given contract IDs. If add_vwap is True, VWAP will be calculated for each trade, incorporating
     all previous trades.

    Args:
        api_client: PowerBot ApiClient
        contract_ids (dict): Dictionary of Contract IDs
        delivery_area (str): EIC Area Code for Delivery Area
        contract_time (str): all, hourly, half-hourly or quarter-hourly
        iteration_delay (float): Optional delay between iterations to prevent hitting API rate limits
        serialize_data (bool): If False, request is sent without serialization. Recommended for large data collections
        add_vwap (bool): If True, additional VWAP parameters will be added to each dataframe
        use_cached_data (bool): If True, function tries to load data from cache wherever possible
        caching (bool): True if data should be cached
        gzip_files (bool): True if cached files should be gzipped
        as_csv (bool): if True, will save files as CSV, additionally to JSON

    Returns:
        Dict{key: DataFrame}: Dictionary of DataFrames
    """
    # Setup
    trades = {}
    missing_contracts = {}
    contract_api = ContractApi(api_client)

    # Load Data
    # Load from Cache
    if use_cached_data:
        # Find __cache__ directory
        cache_path = _find_cache()

        for key, value in contract_ids.items():
            filepath = _get_file_cachepath(api_client, key, delivery_area)
            tmp_df = None

            for i in [".json.gz", ".json"]:
                if cache_path.joinpath(f"{filepath}_trades{i}").exists():
                    tmp_df = pd.read_json(cache_path.joinpath(f"{filepath}_trades{i}"), dtype=False)

            if isinstance(tmp_df, pd.DataFrame):
                tmp_df['api_timestamp'] = pd.to_datetime(tmp_df['api_timestamp'])
                tmp_df['exec_time'] = pd.to_datetime(tmp_df['exec_time'])
                tmp_df = tmp_df.astype({"price": "float64", "trade_id": "object", "contract_id": "object"})
                for i in ["price", "quantity"]:
                    tmp_df[i] = round(tmp_df[i], 2)

                trades[key] = tmp_df

            else:
                # Save Missing Contract IDs
                missing_contracts[key] = value

    contract_ids = missing_contracts if use_cached_data else contract_ids

    for key, value in contract_ids.items():
        public_trade_history = []
        for nr, item in enumerate(value):
            from_public_trade = 0
            more_public_trades = True
            while more_public_trades:
                if serialize_data:
                    public_trades = contract_api.get_public_trades(
                        contract_id=item,
                        delivery_area=delivery_area,
                        offset=from_public_trade,
                        limit=500
                    )
                    public_trade_history.extend([trade.to_dict() for trade in public_trades])

                else:
                    endpoint = f"{api_client.configuration.host}/contract/{item}/{delivery_area}/publictrades?offset={from_public_trade}&limit=500"
                    headers = {"accept": "application/json", "api_key": api_client.configuration.api_key['api_key']}
                    public_trades = json.loads(requests.get(endpoint, headers=headers).text)
                    public_trade_history += public_trades

                if len(public_trades) != 0:
                    from_public_trade += len(public_trades)
                else:
                    more_public_trades = False

        if len(public_trade_history) == 0:
            continue

        df_trades = pd.DataFrame(public_trade_history).sort_values(by=['exec_time'], ascending=True)
        df_trades = df_trades.reset_index(drop=True)
        df_trades['api_timestamp'] = pd.to_datetime(df_trades['api_timestamp'], utc=True)
        df_trades['exec_time'] = pd.to_datetime(df_trades['exec_time'], utc=True)

        trades[key] = df_trades
        sleep(iteration_delay)

    if add_vwap:
        from PowerbotBacktesting.data_processing import calc_trade_vwap
        for k, v in trades.items():
            trades[k] = calc_trade_vwap(api_client=api_client, trade_data={k: v}, contract_time=contract_time,
                                        delivery_area=delivery_area, index="all")

    if caching:
        _cache_data("trade", trades, delivery_area, api_client=api_client, gzip_files=gzip_files, as_csv=as_csv)
    return trades


def get_public_trades_by_days(api_client: ApiClient,
                              previous_days: int,
                              delivery_area: str,
                              time_from: datetime = None,
                              contract_time: str = None,
                              contract_id: str = None) -> Dict[str, pd.DataFrame]:
    """
    Gets the contract ID specified by a timeframe or directly by ID and load all trade data for this contract and all
    contracts in the same timeframe for X previous days.

    Args:
        api_client: PowerBot ApiClient
        time_from (str/ datetime): YYYY-MM-DD hh:mm:ss
        previous_days (int): Amount of previous days to load data for
        delivery_area (str): EIC Area Code for Delivery Area
        contract_time (str): hourly, half-hourly or quarter-hourly
        contract_id (str): specific contract ID

    Returns:
        Dict{key: DataFrame}: Dictionary of DataFrames
    """
    if not time_from and not contract_id:
        raise TypeError("Either time_from and contract_time or a specific contract ID have to be passed.")
    if time_from and not contract_time:
        raise TypeError("If time_from is given, contract_time has to be passed as well.")

    products = None
    use_cached_data = True
    timeframes = {"hourly": 60, "half-hourly": 30, "quarter-hourly": 15}

    try:
        if time_from:
            if isinstance(time_from, str):
                time_from = datetime.strptime(time_from, "%Y-%m-%d %H:%M:%S")
            time_till = time_from + timedelta(minutes=timeframes[contract_time])

        elif contract_id:
            contract = ContractApi(api_client).find_contracts(contract_id=[contract_id])[0]
            if contract.type == "UDC":
                raise TypeError("This function does not work for user defined contracts (UDC).")
            time_from = contract.delivery_start
            time_till = contract.delivery_end
            timeframes = {60: "hourly", 30: "half-hourly", 15: "quarter-hourly"}
            contract_time = timeframes[int((contract.delivery_end - contract.delivery_start).seconds / 60)]
            products = [contract.product]
            use_cached_data = False

        contract_ids = get_contract_ids(api_client=api_client, time_from=time_from, time_till=time_till,
                                        contract_time=contract_time, products=products)

        for _ in range(previous_days):
            time_from -= timedelta(days=1)
            time_till -= timedelta(days=1)

            contract_ids.update(get_contract_ids(api_client=api_client, time_from=time_from, time_till=time_till,
                                                 contract_time=contract_time, products=products))
    except (ValueError, TypeError):
        raise ValueError("Please use correct format: yyyy-mm-dd hh:mm:ss")

    # Get Trade Data
    return get_public_trades(api_client, contract_ids, delivery_area, contract_time, use_cached_data=use_cached_data)


def get_contract_history(api_client: ApiClient,
                         contract_ids: Dict[str, List[str]],
                         delivery_area: str,
                         iteration_delay: float = 0.4,
                         serialize_data: bool = True,
                         use_cached_data: bool = True,
                         caching: bool = True,
                         gzip_files: bool = True,
                         as_csv: bool = False) -> Dict[str, pd.DataFrame]:
    """
    Load contract history for given contract IDs.

    Args:
        api_client: PowerBot ApiClient
        contract_ids (dict): Dictionary of Contract IDs
        delivery_area (str): EIC Area Code for Delivery Area
        iteration_delay (float): Optional delay between iterations to prevent hitting API rate limits
        serialize_data (bool): If False, request is sent without serialization. Recommended for large data collections
        use_cached_data (bool): If True, function tries to load data from cache wherever possible
        caching (bool): True if data should be cached
        gzip_files (bool): True if cached files should be gzipped
        as_csv (bool): if True, will save files as CSV, additionally to JSON

    Returns:
        Dict{key: DataFrame}: Dictionary of DataFrames
    """
    # Setup
    orders = {}
    missing_contracts = {}
    contract_api = ContractApi(api_client)

    if use_cached_data:
        # Find __cache__ directory
        cache_path = _find_cache()
        for key, value in contract_ids.items():
            filepath = _get_file_cachepath(api_client, key, delivery_area)
            tmp_df = None

            for i in [".json.gz", ".json"]:
                if cache_path.joinpath(f"{filepath}_ordhist{i}").exists():
                    tmp_df = pd.read_json(cache_path.joinpath(f"{filepath}_ordhist{i}"), dtype=False,
                                          convert_dates=False)

            if isinstance(tmp_df, pd.DataFrame):
                tmp_df['as_of'] = pd.to_datetime(tmp_df['as_of'])

                cols = {"internal_trades": "object", "contract_id": "object", "auction_price": "float64"}
                cols = {k:v for k,v in cols.items() if k in tmp_df.columns}
                tmp_df = tmp_df.astype(cols, errors='ignore')
                for i in ["best_bid_price", "best_bid_quantity", "best_ask_price", "best_ask_quantity", "last_price",
                          "last_quantity", "total_quantity", "high", "low", "vwap"]:
                    try:
                        tmp_df[i] = round(tmp_df[i], 2)
                    except (TypeError, KeyError):
                        pass

                if "orders" in tmp_df.columns:
                    order_list = tmp_df.orders.tolist()
                    for i in order_list:
                        if "bid" in i and i["bid"]:
                            for b in i["bid"]:
                                for param in ["quantity", "price"]:
                                    b[param] = round(b[param], 2)
                                try:
                                    b["order_entry_time"] = datetime.strptime(b["order_entry_time"],
                                                                          "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=tzutc())
                                except ValueError:
                                    b["order_entry_time"] = datetime.strptime(b["order_entry_time"],
                                                                              "%Y-%m-%dT%H:%M:%SZ").replace(microsecond=0, tzinfo=tzutc())
                        if "ask" in i and i["ask"]:
                            for a in i["ask"]:
                                for param in ["quantity", "price"]:
                                    a[param] = round(a[param], 2)
                                try:
                                    a["order_entry_time"] = datetime.strptime(a["order_entry_time"],
                                                                              "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=tzutc())
                                except ValueError:
                                    a["order_entry_time"] = datetime.strptime(a["order_entry_time"],
                                                                          "%Y-%m-%dT%H:%M:%SZ").replace(microsecond=0, tzinfo=tzutc())

                    tmp_df["orders"] = order_list

                orders[key] = tmp_df

            else:
                # Save Missing Contract IDs
                missing_contracts[key] = value

    contract_ids = missing_contracts if use_cached_data else contract_ids

    for key, value in contract_ids.items():
        public_contract_history = []
        for nr, item in enumerate(value):
            more_revisions = True
            from_revision = 0

            while more_revisions:
                if serialize_data:
                    contract_history = contract_api.get_contract_history(
                        contract_id=item,
                        delivery_area=delivery_area,
                        with_orders=True,
                        with_owntrades=False,
                        offset=from_revision,
                        limit=150
                    )
                    public_contract_history.extend([trade.to_dict() for trade in contract_history])

                else:
                    endpoint = f"{api_client.configuration.host}/contract/{item}/{delivery_area}/history?offset={from_revision}&limit=150&with_owntrades=false&with_signals=false&with_orders=true"
                    headers = {"accept": "application/json", "api_key": api_client.configuration.api_key['api_key']}
                    contract_history = json.loads(requests.get(endpoint, headers=headers).text)
                    public_contract_history += contract_history

                if len(contract_history) != 0:
                    from_revision += len(contract_history)
                else:
                    more_revisions = False

        if len(public_contract_history) == 0:
            continue

        df_history = pd.DataFrame(public_contract_history).sort_values(by=['as_of'], ascending=True)
        df_history = df_history.reset_index(drop=True)
        df_history['as_of'] = pd.to_datetime(df_history['as_of'], utc=True)
        df_history.drop(columns=["auction_price", "internal_trades"], inplace=True, errors="ignore")

        orders[key] = df_history
        sleep(iteration_delay)

    if caching:
        _cache_data("order", orders, delivery_area, api_client=api_client, gzip_files=gzip_files, as_csv=as_csv)
    return orders


def get_signals(api_client: ApiClient,
                time_from: datetime,
                time_till: datetime,
                portfolio_id: List[str] = None) -> List[Signal]:
    """
    Function gathers all Signals received by the API in the specified time period and gathers them in a list.

    Args:
        api_client: PowerBot ApiClient
        time_from (str/ datetime): YYYY-MM-DD or YYYY-MM-DD hh:mm:ss
        time_till (str/ datetime): YYYY-MM-DD or YYYY-MM-DD hh:mm:ss
        portfolio_id: List of all portfolios that signals should be loaded from

    Returns:
        List[Signal]
    """
    signals = []
    more_signals = True
    offset = 0
    params = {"portfolio_id": portfolio_id} if portfolio_id else {}

    while more_signals:
        new_signals = SignalsApi(api_client).get_signals(received_from=time_from, received_to=time_till, offset=offset,
                                                         limit=500, **params)
        if len(new_signals):
            signals += new_signals
            offset += len(new_signals)
        else:
            more_signals = False
        sleep(0.2)

    return signals


def get_own_trades(api_client: ApiClient,
                   time_from: datetime,
                   time_till: datetime,
                   delivery_area: str = None,
                   portfolio_id: List[str] = None) -> List[Trade]:
    """
    Function to collect all Own Trades for the defined time period, either specific to portfolio and/or delivery area
    or all portfolios and delivery areas used API key has access to.

    Args:
        api_client: PowerBot ApiClient
        time_from (str/ datetime): YYYY-MM-DD or YYYY-MM-DD hh:mm:ss
        time_till (str/ datetime): YYYY-MM-DD or YYYY-MM-DD hh:mm:ss
        delivery_area (str): EIC Area Code for Delivery Area
        portfolio_id List[str]: List of specific portfolio IDs to load trades from. If left out, will load from all IDs.

    Returns:
        List[Trade]
    """
    own_trades = []
    more_own_trades = True
    offset = 0
    params = {}
    if portfolio_id:
        params["portfolio_id"] = portfolio_id
    if delivery_area:
        params["delivery_area"] = delivery_area

    while more_own_trades:
        new_own_trades = TradesApi(api_client).get_trades(delivery_within_start=time_from,
                                                          delivery_within_end=time_till,
                                                          offset=offset,
                                                          limit=500,
                                                          **params)
        if len(new_own_trades):
            own_trades += new_own_trades
            offset += len(new_own_trades)
        else:
            more_own_trades = False
        sleep(0.2)

    return own_trades


def get_internal_trades(api_client: ApiClient,
                        time_from: datetime,
                        time_till: datetime,
                        delivery_area: str = None,
                        portfolio_id: List[str] = None) -> List[InternalTrade]:
    """
    Function to collect all Internal Trades for the defined time period, either specific to portfolio and/or delivery
    area or all portfolios and delivery areas used API key has access to.

    Args:
        api_client: PowerBot ApiClient
        time_from (str/ datetime): YYYY-MM-DD or YYYY-MM-DD hh:mm:ss
        time_till (str/ datetime): YYYY-MM-DD or YYYY-MM-DD hh:mm:ss
        delivery_area (str): EIC Area Code for Delivery Area
        portfolio_id List[str]: List of specific portfolio IDs to load trades from. If left out, will load from all IDs.

    Returns:
        List[InternalTrade]
    """
    internal_trades = []
    more_internal_trades = True
    offset = 0
    params = {}
    if portfolio_id:
        params["portfolio_id"] = portfolio_id
    if delivery_area:
        params["delivery_area"] = delivery_area

    while more_internal_trades:
        new_internal_trades = TradesApi(api_client).get_internal_trades(delivery_within_start=time_from,
                                                                        delivery_within_end=time_till,
                                                                        offset=offset,
                                                                        limit=100,
                                                                        **params)

        if len(new_internal_trades):
            internal_trades += new_internal_trades
            offset += len(new_internal_trades)
        else:
            more_internal_trades = False
        sleep(0.2)

    return internal_trades


def get_own_orders(api_client: ApiClient,
                   delivery_area: str = None,
                   portfolio_id: List[str] = None,
                   active_only: bool = False) -> List[OwnOrder]:
    """
    Function to collect all available Own Orders, either specific to portfolio and/or delivery area or all portfolios
    and delivery areas used API key has access to.

    Args:
        api_client: PowerBot ApiClient
        delivery_area (str): EIC Area Code for Delivery Area
        portfolio_id List[str]: List of specific portfolio IDs to load trades from. If left out, will load from all IDs.
        active_only (bool):  True if only active orders should be loaded. If False, loads also hibernate and inactive.

    Returns:
        List[OwnOrder]
    """
    own_orders = []
    more_own_orders = True
    offset = 0
    params = {}
    if portfolio_id:
        params["portfolio_id"] = portfolio_id
    if delivery_area:
        params["delivery_area"] = delivery_area
    if active_only:
        params["active_only"] = active_only

    while more_own_orders:
        new_own_orders = OrdersApi(api_client).get_own_orders(offset=offset,
                                                              limit=500,
                                                              **params)
        if len(new_own_orders):
            own_orders += new_own_orders
            offset += len(new_own_orders)
        else:
            more_own_orders = False
        sleep(0.2)

    return own_orders
