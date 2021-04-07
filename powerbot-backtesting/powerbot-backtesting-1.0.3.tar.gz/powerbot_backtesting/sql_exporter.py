import logging
import json
import urllib.parse
import pandas as pd
from typing import List, Dict, Tuple, Union
from datetime import datetime
from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import NoSuchModuleError, InterfaceError, ProgrammingError, OperationalError, TimeoutError

from powerbot_backtesting.utils.constants import *
from powerbot_backtesting.exceptions import SQLExporterError

try:
    from swagger_client import OwnOrder, Trade, InternalTrade, Signal
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "You need an up-to-date swagger client in the top level of your project directory to run this package!")


class PowerBotSQLExporter:
    """
    Class to provide quick and easy functions to load data from a SQL database.

    Instructions for passing arguments to export functions:
        - String
            If keyword argument is a string, it will be simply compared with '='. Optionally, a mathematical/ SQL
            operator (LIKE, <, <=, >, >=, <>) can be passed within the string. This operator will be used instead of '='.

            Example:
                best_bid='> 0.00' -> best_bid > 0.00 / as_of="> 2020-09-20 00:00:00" -> as_of > '2020-09-20 00:00:00'

        - Tuple
            If keyword argument is a tuple, it will be checked, if parameter is one of the elements of the tuple.

            Example:
                exchange=("Epex","NordPool") -> exchange IN ('Epex','NordPool')

        - List
            If keyword argument is a list, each element will be checked if it is in the parameter.

            Example:
                portfolio_ids=["TP1","TP2"] -> (portfolio_id LIKE '%TP1%' OR portfolio_id LIKE '%TP2%')

        - Dictionary
            If keyword argument is a dictionary, all values will be extracted and put into a tuple. Afterwards, the
            behaviour is the same as with tuples.

            Example:
                exchange={1:"Epex",2:"NordPool"} -> exchange IN ("Epex","NordPool")

        - Datetime
            If keyword argument is a datetime, parameter will be searched for the exact time of the datetime argument.
            This will in most cases not provide a satisfying result, therefore it is recommended to pass a datetime as
            a string with an operator in front.

            Example:
                as_of=datetime.datetime(2020, 9, 30, 10, 0, 0) -> as_of = '2020-09-30 10:00:00'
    """
    SQL_ERRORS = (
        InterfaceError,
        OperationalError,
        ProgrammingError,
        TimeoutError,
    )

    def __init__(self, db_type, user, password, host, database, port):
        # Set Parameters
        self.db_type = db_type
        self.user = urllib.parse.quote(user)
        self.password = urllib.parse.quote(password)
        self.host = host
        self.database = database
        self.port = port

        # Logging Setup
        logging.basicConfig(format="PowerBot_SQL_Exporter %(asctime)s %(levelname)-8s %(message)s",
                            level=logging.INFO)
        self.logger = logging.getLogger()

        # Initialize Connection
        self.engine = self._create_sql_engine()

    def _install_packages(self):
        """
        Tests if required packages for chosen SQL database type are available
        """
        db_packages = {"mysql": ["mysql-connector-python"],
                       "postgresql": ["psycopg2"],
                       "oracle": ["cx-Oracle"],
                       "mssql": ["pyodbc"],
                       "amazon_redshift": ["sqlalchemy-redshift", "psycopg2"],
                       "apache_drill": ["sqlalchemy-drill"],
                       "apache_druid": ["pydruid"],
                       "apache_hive": ["PyHive"],
                       "apache_solr": ["sqlalchemy-solr"],
                       "cockroachdb": ["sqlalchemy-cockroachdb", "psycopg2"],
                       "cratedb": ["crate-python"],
                       "exasolution": ["sqlalchemy_exasol", "pyodbc"],
                       "firebird": ["sqlalchemy-firebird"],
                       "ibm_db2": ["ibm_db_sa"],
                       "monetdb": ["sqlalchemy_monetdb"],
                       "snowflake": ["snowflake-sqlalchemy"],
                       "teradata_vantage": ["teradatasqlalchemy"]}

        self.logger.info("Now installing the following necessary package(s):\n"
                         f"{db_packages[self.db_type]}")

        import subprocess
        import sys
        for pkg in db_packages[self.db_type]:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

        return self._create_sql_engine()

    def _create_sql_engine(self):
        """
        Initializes connection to SQL database
        """
        db_types = {"mysql": ["mysql", "mysqlconnector"],
                    "postgresql": ["postgresql", "psycopg2"],
                    "oracle": ["oracle", "cx_oracle"],
                    "mssql": ["mssql", "pyodbc"],
                    "amazon_redshift": ["redshift", "psycopg2"],
                    "apache_drill": ["drill", "sadrill"],
                    "apache_druid": ["druid"],
                    "apache_hive": ["hive"],
                    "apache_solr": ["solr"],
                    "cockroachdb": ["cockroachdb"],
                    "cratedb": ["crate"],
                    "exasolution": ["exa", "pyodbc"],
                    "firebird": ["firebird"],
                    "ibm_db2": ["db2", "ibm_db"],
                    "monetdb": ["monetdb"],
                    "snowflake": ["snowflake"],
                    "teradata_vantage": ["teradatasql"]}

        if self.port:
            try:
                if len(db_types[self.db_type]) == 2:
                    engine = create_engine(
                        f'{db_types[self.db_type][0]}+{db_types[self.db_type][1]}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')
                else:
                    engine = create_engine(
                        f'{db_types[self.db_type][0]}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')
            except:
                pass
        try:
            if len(db_types[self.db_type]) == 2:
                engine = create_engine(
                    f'{db_types[self.db_type][0]}+{db_types[self.db_type][1]}://{self.user}:{self.password}@{self.host}/{self.database}')
            else:
                engine = create_engine(
                    f'{db_types[self.db_type][0]}://{self.user}:{self.password}@{self.host}/{self.database}')

        except (NoSuchModuleError, ModuleNotFoundError):
            self.logger.info("You currently do not have all the necessary packages installed to access a database of"
                             f" type {self.db_type}.")
            self._install_packages()

        except ProgrammingError:
            self.logger.error("Could not establish connection to database. Please recheck your credentials!")

        except InterfaceError:
            self.logger.error("Database is not available at the moment!")

        except Exception as e:
            raise SQLExporterError(f"Could not establish connection to database. Reason: \n{e}")

        # Test connection
        engine.connect()

        self.logger.info(f"Connection to database '{self.database}' with user '{self.user}' established")
        self.logger.info("Connection ready to export data")

        return engine

    @contextmanager
    def _get_session(self):
        try:
            session = Session(bind=self.engine)
        except self.SQL_ERRORS:
            session = Session(bind=self._create_sql_engine())
        try:
            yield session
        finally:
            session.close()

    def export_contracts(self, as_dataframe: bool = True, **kwargs) -> pd.DataFrame:
        """
        Exports contracts from SQL database. To use different mathematical/SQL operators, pass keyworded arguments
        as strings and include the desired operator followed by a space (e.g. revisions='<> 0').

        Following operators can be passed:
        LIKE, <, <=, >, >=, <>

        Following parameters can be passed as optional keyworded arguments:
        exchange, contract_id, product, type, undrlng_contracts, name, delivery_start, delivery_end, delivery_areas,
        predefined, duration, delivery_units

        Args:
            as_dataframe (bool): If False -> returns list
            **kwargs: any additional fields of SQL table

        Returns:
            List/ DataFrame: SQL query
        """
        allowed_kwargs = ["name", "delivery_areas", "delivery_start", "delivery_end", "delivery_areas", "type",
                          "predefined", "duration", "delivery_units", "contract_id", "exchange", "product",
                          "undrlng_contracts"]

        sql_params = self._handle_sql_args(kwargs, allowed_kwargs)

        with self._get_session() as session:
            result = session.execute(f"SELECT * FROM contracts{sql_params}").fetchall()

        if as_dataframe:
            output = pd.DataFrame(result)
            output = output.rename(columns={0: 'exchange', 1: 'contract_id', 2: 'product', 3: 'type', 4:'undrlng_contracts',
                                            5: 'name', 6: 'delivery_start', 7: 'delivery_end', 8: 'delivery_areas',
                                            9: 'predefined', 10: 'duration', 11: 'delivery_units', 12: 'details'})
            return output

        return result

    def export_contract_ids(self, time_from: datetime,
                            time_till: datetime,
                            delivery_area: str,
                            contract_time: str = "all",
                            exchange: str = "epex",
                            as_list: bool = False) -> Dict[str, List[str]]:
        """
            Returns dictionary of contract IDs in a format compatible with backtesting pipeline.

        Args:
            time_from (datetime): yyyy-mm-dd hh:mm:ss
            time_till (datetime): yyyy-mm-dd hh:mm:ss
            delivery_area (str): EIC-Code
            contract_time (str): all, hourly, half-hourly or quarter-hourly
            exchange (str): Name of exchange in lowercase
            as_list (bool): True if output should be list of contract IDs

        Returns:
            Dict{key: (List[str])}: Dictionary of Contract IDs
        """
        if not isinstance(time_from, datetime) or not isinstance(time_till, datetime):
            raise SQLExporterError("Please use datetime format for time_from & time_till!")

        products = {"hourly": ("XBID_Hour_Power", "Intraday_Hour_Power", "GB_Hour_Power", "P60MIN"),
                    "half-hourly": ("XBID_Half_Hour_Power", "Intraday_Half_Hour_Power", "GB_Half_Hour_Power", "P30MIN"),
                    "quarter-hourly": ("XBID_Quarter_Hour_Power", "Intraday_Quarter_Hour_Power", "GB_Quarter_Hour_Power", "P15MIN"),
                    "continuous": ("Continuous_Power_Peak",)}
        products["all"] = products["hourly"] + products["quarter-hourly"] + products["half-hourly"] + products["continuous"]

        with self._get_session() as session:
            result = session.execute(f"SELECT delivery_start, delivery_end, contract_id FROM contracts "
                                     f"WHERE delivery_start >= '{time_from}' "
                                     f"AND delivery_end <= '{time_till}' "
                                     f"AND delivery_areas LIKE '%{delivery_area}%' "
                                     f"AND product IN {products[contract_time]} "
                                     f"AND exchange = '{exchange}'").fetchall()
            if not result:
                result = session.execute(f"SELECT delivery_start, delivery_end, contract_id FROM contracts "
                                         f"WHERE delivery_start >= '{time_from}' "
                                         f"AND delivery_end <= '{time_till}' "
                                         f"AND product IN {products[contract_time]} "
                                         f"AND exchange = '{exchange}'").fetchall()

        if not as_list:
            contract_ids = {f"{i[0].strftime(DATE_YMD_TIME_HM)} - {i[1].strftime(TIME_HM)}": [] for i in result}
            for i in result:
                contract_ids[f"{i[0].strftime(DATE_YMD_TIME_HM)} - {i[1].strftime(TIME_HM)}"].append(i[2])

            # Quality Check
            if not all(i for i in contract_ids.values()):
                raise SQLExporterError("There is no contract data for the specified timeframe!")
        else:
            contract_ids = [i for i in result]

        self.logger.info("Successfully exported contract ids")
        return contract_ids

    def export_public_trades(self, as_dataframe: bool = True,
                             delivery_area: List[str] = None,
                             **kwargs) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """
        Exports trades from SQL database. To use different mathematical/SQL operators, pass keyworded arguments
        as strings and include the desired operator followed by a space (e.g. price='<> 0.00').

        Following operators can be passed:
        LIKE, <, <=, >, >=, <>

        Following parameters can be passed as optional keyworded arguments (kwargs):
        price, quantity, prc_x_qty, exchange, contract_id, trade_id, exec_time, api_timestamp, self_trade

        Args:
            as_dataframe (bool): If False -> returns list
            delivery_area Tuple[str]: Multiple delivery areas inside a tuple. Single del. area can be passed as a string
            **kwargs: any additional fields of SQL table

        Returns:
            List/ DataFrame: SQL query
        """
        allowed_kwargs = ["price", "quantity", "prc_x_qty", "exchange", "contract_id", "trade_id", "exec_time",
                          "api_timestamp", "self_trade"]

        sql_params = self._handle_sql_args(kwargs, allowed_kwargs)
        if delivery_area:
            for i in delivery_area:
                sql_params += f" AND (buy_delivery_area = '{i}' OR sell_delivery_area = '{i}')"

        with self._get_session() as session:
            result = session.execute(f"SELECT * FROM public_trades{sql_params}").fetchall()

        if as_dataframe:
            output = pd.DataFrame(result)
            if not output.empty:
                output = output.rename(columns={0: 'exchange', 1: 'contract_id', 2: 'trade_id', 3: 'api_timestamp',
                                                4: 'exec_time', 5: 'buy_delivery_area', 6: 'sell_delivery_area',
                                                7: 'price',  8: 'quantity', 9: 'prc_x_qty', 10: "currency", 11: 'self_trade'})
                if not delivery_area:
                    raise SQLExporterError("Please specify at least one delivery area!")

                output['api_timestamp'] = pd.to_datetime(output['api_timestamp'], utc=True)
                output['exec_time'] = pd.to_datetime(output['exec_time'], utc=True)

                self.logger.info("Successfully exported trades")
                return self._convert_dataframe("trades", output)
            else:
                raise SQLExporterError("There is no trade data for the specified timeframe!")

        self.logger.info("Successfully exported trades")

        return result

    def export_own_trades(self, delivery_area: List[str] = None,
                          as_dataframe: bool = True,
                          as_objects: bool = False,
                          **kwargs) -> Union[pd.DataFrame, List[Trade]]:
        """
        Exports Own Trades from SQL database. To use different mathematical/SQL operators, pass keyworded arguments
        as strings and include the desired operator followed by a space (e.g. position_short='<> 0.00').

        Following operators can be passed:
        LIKE, <, <=, >, >=, <>

        Following parameters can be passed as optional keyworded arguments (kwargs):
        exchange, contract_id, contract_name, prod, delivery_start, delivery_end, trade_id, api_timestamp, exec_time,
        buy, sell, price, quantity, state, buy_delivery_area, sell_delivery_area, buy_order_id, buy_clOrderId, buy_txt,
        buy_user_code, buy_member_id, buy_aggressor_indicator, buy_portfolio_id, sell_order_id, sell_clOrderId,
        sell_txt, sell_user_code, sell_member_id, sell_aggressor_indicator, sell_portfolio_id, self_trade, pre_arranged,
        pre_arrange_type

        Args:
            delivery_area Tuple[str]: Multiple delivery areas inside a tuple. Single del. area can be passed as a string
            as_dataframe (bool): True if output should be DataFrame
            as_objects (bool): True if output should be list of OwnTrades
            **kwargs: any additional fields of SQL table

        Returns:
            List: SQL query
        """

        allowed_kwargs = ["exchange", "contract_id", "contract_name", "prod", "delivery_start", "delivery_end",
                          "trade_id",
                          "api_timestamp", "exec_time", "buy", "sell", "price", "quantity", "state",
                          "buy_delivery_area",
                          "sell_delivery_area", "buy_order_id", "buy_clOrderId", "buy_txt", "buy_user_code",
                          "buy_member_id",
                          "buy_aggressor_indicator", "buy_portfolio_id", "sell_order_id", "sell_clOrderId", "sell_txt",
                          "sell_user_code", "sell_member_id", "sell_aggressor_indicator", "sell_portfolio_id",
                          "self_trade",
                          "pre_arranged", "pre_arrange_type"]

        sql_params = self._handle_sql_args(kwargs, allowed_kwargs)

        if delivery_area:
            for i in delivery_area:
                sql_params += f" AND (buy_delivery_area = '{i}' OR sell_delivery_area = '{i}')"

        with self._get_session() as session:
            result = session.execute(f"SELECT * FROM own_trades{sql_params}").fetchall()

        self.logger.info("Successfully exported own trades")

        # Convert data back to Trade objects
        if result and as_objects:
            own_trades = [Trade(exchange=i[0],
                                contract_id=i[1],
                                contract_name=i[2],
                                prod=i[3],
                                delivery_start=i[4],
                                delivery_end=i[5],
                                trade_id=i[6],
                                api_timestamp=i[7],
                                exec_time=i[8],
                                buy=i[9],
                                sell=i[10],
                                price=i[11],
                                quantity=i[12],
                                delivery_area=i[13],
                                state=i[14],
                                buy_delivery_area=i[15],
                                sell_delivery_area=i[16],
                                buy_order_id=i[17],
                                buy_cl_order_id=i[18],
                                buy_txt=i[19],
                                buy_user_code=i[20],
                                buy_member_id=i[21],
                                buy_aggressor_indicator=i[22],
                                buy_portfolio_id=i[23],
                                sell_order_id=i[24],
                                sell_cl_order_id=i[25],
                                sell_txt=i[26],
                                sell_user_code=i[27],
                                sell_member_id=i[28],
                                sell_aggressor_indicator=i[29],
                                sell_portfolio_id=i[30],
                                self_trade=i[31],
                                pre_arranged=i[32],
                                pre_arrange_type=i[33])
                          for i in result]
            return own_trades

        if result and as_dataframe:
            return pd.DataFrame(result)

        return result

    def export_internal_trades(self, delivery_area: Tuple[str] = None,
                               as_dataframe: bool = True,
                               as_objects: bool = False,
                               **kwargs) -> Union[pd.DataFrame, List[InternalTrade]]:
        """
        Exports Internal Trades from SQL database. To use different mathematical/SQL operators, pass keyworded arguments
        as strings and include the desired operator followed by a space (e.g. position_short='<> 0.00').

        Following operators can be passed:
        LIKE, <, <=, >, >=, <>

        Following parameters can be passed as optional keyworded arguments (kwargs):
        exchange, contract_id, contract_name, prod, delivery_start, delivery_end, internal_trade_id, api_timestamp,
        exec_time, price, quantity, state, buy_delivery_area, sell_delivery_area, buy_order_id, buy_clOrderId, buy_txt,
        buy_aggressor_indicator, buy_portfolio_id, sell_order_id, sell_clOrderId, sell_txt, sell_aggressor_indicator,
        sell_portfolio_id

        Args:
            delivery_area Tuple[str]: Multiple delivery areas inside a tuple. Single del. area can be passed as a string
            as_dataframe (bool): True if output should be DataFrame
            as_objects (bool): True if output should be list of InternalTrades
            **kwargs: any additional fields of SQL table

        Returns:
            List: SQL query
        """
        allowed_kwargs = ["exchange", "contract_id", "contract_name", "prod", "delivery_start", "delivery_end",
                          "internal_trade_id", "api_timestamp", "exec_time", "price", "quantity", "state",
                          "buy_delivery_area", "sell_delivery_area", "buy_order_id", "buy_clOrderId", "buy_txt",
                          "buy_aggressor_indicator", "buy_portfolio_id", "sell_order_id", "sell_clOrderId", "sell_txt",
                          "sell_aggressor_indicator", "sell_portfolio_id"]

        sql_params = self._handle_sql_args(kwargs, allowed_kwargs)

        if delivery_area:
            for i in delivery_area:
                sql_params += f" AND (buy_delivery_area = '{i}' OR sell_delivery_area = '{i}')"

        with self._get_session() as session:
            result = session.execute(f"SELECT * FROM internal_trades{sql_params}").fetchall()

        self.logger.info("Successfully exported internal trades")

        # Convert data back to InternalTrade objects
        if result and as_objects:
            internal_trades = [InternalTrade(exchange=i[0],
                                             contract_id=i[1],
                                             contract_name=i[2],
                                             prod=i[3],
                                             delivery_start=i[4],
                                             delivery_end=i[5],
                                             internal_trade_id=i[6],
                                             api_timestamp=i[7],
                                             exec_time=i[8],
                                             price=i[9],
                                             quantity=i[10],
                                             buy_delivery_area=i[11],
                                             sell_delivery_area=i[12],
                                             buy_order_id=i[13],
                                             buy_cl_order_id=i[14],
                                             buy_txt=i[15],
                                             buy_aggressor_indicator=i[16],
                                             buy_portfolio_id=i[17],
                                             sell_order_id=i[18],
                                             sell_cl_order_id=i[19],
                                             sell_txt=i[20],
                                             sell_aggressor_indicator=i[21],
                                             sell_portfolio_id=i[22])
                               for i in result]
            return internal_trades

        if result and as_dataframe:
            return pd.DataFrame(result)

        return result

    def export_contract_history(self, as_dataframe: bool = True,
                                **kwargs) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """
        Exports contract revisions from SQL database. To use different mathematical/SQL operators, pass keyworded arguments
        as strings and include the desired operator followed by a space (e.g. best_bid='<> 0.00').

        Following operators can be passed:
        LIKE, <, <=, >, >=, <>

        Following parameters can be passed as optional keyworded arguments:
        exchange, contract_id, exchange, delivery_area, revision_no, as_of, best_bid, best_bid_qty, best_ask,
        best_ask_qty, vwap, high, low, last_price, last_qty, last_trade_time, volume, delta

        Args:
            as_dataframe (bool): If False -> returns list
            **kwargs: any additional fields of SQL table

        Returns:
            List/ DataFrame: SQL query
        """
        allowed_kwargs = ["exchange", "contract_id", "delivery_area", "revision_no", "as_of", "best_bid",
                          "best_bid_qty", "best_ask", "best_ask_qty", "vwap", "high", "low", "last_price",
                          "last_qty", "last_trade_time", "volume", "delta"]

        sql_params = self._handle_sql_args(kwargs, allowed_kwargs)

        with self._get_session() as session:
            result = session.execute(f"SELECT * FROM contract_revisions{sql_params}").fetchall()

        if as_dataframe:
            output = pd.DataFrame(result)
            if not output.empty:
                output = output.rename(columns={0: 'exchange', 1: 'contract_id', 2: 'delivery_area', 3: 'revision_no',
                                                4: 'as_of', 5: 'best_bid', 6: 'best_bid_qty', 7: 'best_ask',
                                                8: 'best_ask_qty', 9: 'vwap', 10: 'high',
                                                11: 'low', 12: 'last_price', 13: 'last_qty', 14: 'volume', 15: 'delta',
                                                16: 'bids', 17: 'asks'})
                if not "delivery_area" in kwargs:
                    raise SQLExporterError("Please specify one specific delivery area!")
                self.logger.info("Successfully exported revisions")
                return self._convert_dataframe("orders", output)
            else:
                raise SQLExporterError("There is no order data for the specified timeframe!")

        self.logger.info("Successfully exported revisions")

        return result

    def export_signals(self, time_from: datetime,
                       time_till: datetime,
                       as_dataframe: bool = True,
                       as_objects: bool = False,
                       **kwargs) -> pd.DataFrame:
        """
        Exports signals from SQL database. To use different mathematical/SQL operators, pass keyworded arguments
        as strings and include the desired operator followed by a space (e.g. position_short='<> 0.00').

        Following operators can be passed:
        LIKE, <, <=, >, >=, <>

        Following parameters can be passed as optional keyworded arguments:
        id, source, received_at, revision, delivery_areas, portfolio_ids, tenant_id, position_short,
        position_long, value

        Args:
            time_from (datetime): yyyy-mm-dd hh:mm:ss
            time_till (datetime): yyyy-mm-dd hh:mm:ss
            as_dataframe (bool): True if output should be DataFrame
            as_objects (bool): True if output should be list of Signals
            **kwargs: any additional fields of SQL table

        Returns:
            List: SQL query
        """
        allowed_kwargs = ["id", "source", "received_at", "revision", "delivery_areas", "portfolio_ids", "tenant_id",
                          "position_short", "position_long", "value"]

        sql_params = self._handle_sql_args(kwargs, allowed_kwargs)
        sql_op = "AND" if sql_params else "WHERE"

        with self._get_session() as session:
            result = session.execute(f"SELECT * FROM signals{sql_params} "
                                     f"{sql_op} delivery_start >= '{time_from}' "
                                     f"AND delivery_end <= '{time_till}'").fetchall()

        self.logger.info("Successfully exported signals")

        # Convert data back to InternalTrade objects
        if result and as_objects:
            signals = [Signal(id=i[0],
                              source=i[1],
                              received_at=i[2],
                              revision=i[3],
                              delivery_start=i[4],
                              delivery_end=i[5],
                              portfolio_ids=i[6],
                              tenant_id=i[7],
                              position_short=i[8],
                              position_long=i[9],
                              value=i[10])
                       for i in result]

            return signals

        if result and as_dataframe:
            return pd.DataFrame(result)

        return result

    def send_raw_sql(self, sql_statement:str):
        """
        Function allows for raw SQL queries to be sent to the database.

        Args:
            sql_statement (str): SQL query

        Returns:

        """
        with self._get_session() as session:
            try:
                result = session.execute(sql_statement).fetchall()
            except self.SQL_ERRORS as e:
                return self.logger.error(e)
        return result

    def _handle_sql_args(self, kwargs, allowed_kwargs: List[str]) -> str:
        """
        Handles incoming arguments by adjusting them to be compatible with SQL.

        Args:
            kwargs: **kwargs of export functions
            allowed_kwargs (list[str]): list of allowed kwargs

        Returns:
            str: SQL request
        """
        if not all(arg for arg in kwargs.values()):
            print(kwargs)
            print([arg for arg in kwargs.values()])
            raise SQLExporterError("Some of your input values are invalid or empty!")
        sql_params = ""
        operators = ["LIKE", "<", "<=", ">", ">=", "<>"]

        for keyword, argument in kwargs.items():
            op = "="
            sql_statement = "WHERE" if sql_params == "" else "AND"

            if keyword not in allowed_kwargs:
                raise SQLExporterError(f"{keyword} not in allowed keywords. Allowed keywords: {allowed_kwargs}")
            else:
                if isinstance(argument, str):
                    # Check For SQL Commands Or Mathematical Operators
                    if any(x in argument for x in operators):
                        if len(argument.split(" ")) > 2:
                            op = argument.split(" ")[0]
                            argument = argument.replace(f"{op} ", "")
                        else:
                            op, argument = argument.split(" ")
                        if op == "LIKE":
                            argument = f"%{argument}%"
                        try:
                            datetime.strptime(argument, DATE_YMD_TIME_HMS)
                        except:
                            pass
                elif isinstance(argument, tuple):
                    if len(argument) == 1:
                        argument = argument[0]
                    else:
                        op = "IN"
                elif isinstance(argument, list):
                    for nr, element in enumerate(argument):
                        if not nr:
                            if element == argument[-1]:
                                sql_params += f" {sql_statement} ({keyword} LIKE '%{element}%')"
                            else:
                                sql_params += f" {sql_statement} ({keyword} LIKE '%{element}%'"
                        elif element == argument[-1]:
                            sql_params += f" OR {keyword} LIKE '%{element}%')"
                        else:
                            sql_params += f" OR {keyword} LIKE '%{element}%'"
                    continue

                elif isinstance(argument, dict):
                    op = "IN"
                    temp_list = []
                    for value in argument.values():
                        for item in value:
                            temp_list.append(item)
                    argument = tuple(temp_list)
                try:
                    if not isinstance(argument, tuple) and keyword != "contract_id":
                        argument = float(argument)
                    sql_params += f" {sql_statement} {keyword} {op} {argument}"
                except:
                    sql_params += f" {sql_statement} {keyword} {op} '{argument}'"

        return sql_params

    def _convert_dataframe(self, df_type: str, dataframe: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Function to convert dataframe to required format to be processed by backtesting data pipeline.

        Args:
            df_type (str): orders/trades/orderbooks
            dataframe (DataFrame): DataFrame containing exported Data

        Returns:
            Dict{key: DataFrame}: Dictionary of DataFrames
        """
        output = {}

        contract_ids = dataframe.contract_id.unique().tolist()
        contracts = self.export_contracts(contract_id=contract_ids)

        if df_type == "trades":
            dataframe = dataframe.astype({'price': 'float', 'quantity': 'float'})

        elif df_type == "orders":
            bids = [json.loads(i) if i else None for i in dataframe.bids.tolist()]
            asks = [json.loads(i) if i else None for i in dataframe.asks.tolist()]

            dataframe.drop(columns=["bids", "asks"])
            orders = []
            for nr, val in enumerate(bids):
                orders.append({"bid": val, "ask": asks[nr]})
            dataframe["orders"] = orders

        for row_nr, row_id in enumerate(contracts.contract_id):
            key = f"{contracts.iloc[row_nr].delivery_start.strftime(DATE_YMD_TIME_HM)} - " \
                  f"{contracts.iloc[row_nr].delivery_end.strftime(TIME_HM)}"

            if not key in [*output]:
                output[key] = dataframe[dataframe["contract_id"] == row_id]
            else:
                output[key].append(dataframe[dataframe["contract_id"] == row_id])

        return output
