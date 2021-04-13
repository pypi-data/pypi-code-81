import datetime
import numpy as np
import pandas as pd
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine


# !conda install -y -c conda-forge pyarrow
# set the sf account name

class Snowflakeq:
    
    sf_account = ''
    
    def __init__(self, sf_account='ra45066.eu-west-1'):

        self.sf_account = sf_account

    def is_valid_date(self, date_txt):
        res = True

        try:
            datetime.datetime.strptime(date_txt, '%Y-%m-%d')
        except ValueError:
            res = False

        return res

    def get_sf_con(self, customer_name, password, role=''):
        # Connecting to Snowflake using the default authenticator
        engine = create_engine(URL(
            account=self.sf_account,
            user=customer_name,
            password=password,
            database=customer_name,
            schema='PUBLIC',
            warehouse=customer_name,
            role=customer_name if role == '' else role,
        ))

        return engine

    def exec_sf(self, cmd, customer_name, password, role=''):
        # get the snowflake engine object
        sf_eng = self.get_sf_con(customer_name, password, role)

        res = False

        try:
            # connect to snowflake
            con = sf_eng.connect()

            # execute the query
            con.execute(cmd)

            res = True

        except Exception as e:
            print("Error!")
            print(str(e))

        finally:
            # close the connection
            con.close()
            sf_eng.dispose()

        return res

    def exec_sf_q(self, cmd, customer_name, password, role=''):
        # get the snowflake engine object
        sf_eng = self.get_sf_con(customer_name, password, role)

        res = None
        try:
            # connect to snowflake
            con = sf_eng.connect()

            # execute the query
            res = pd.read_sql_query(cmd, con)

            # change column names to uppercase
            res.columns = res.columns.str.upper()

        except Exception as e:
            print("Error!")
            print(str(e))

        finally:
            # close the connection
            con.close()
            sf_eng.dispose()

        return res

    def get_data_from_sf(self, view_name, customer_name, password, now_date='2021-01-01', from_date='2018-01-01', min_last_order_date='2021-01-01', last_order_x_month_ago=0, 
                         num_of_month_for_target=3, order_by='', limit=0, offset=0, ext_var_cmd=''):
        # get the snowflake engine object
        sf_eng = self.get_sf_con(customer_name, password)

        # validate variables
        if not self.is_valid_date(now_date):
            now_date = '2021-01-01'

        if not self.is_valid_date(from_date):
            from_date = '2018-01-01'

        if not self.is_valid_date(min_last_order_date):
            min_last_order_date = '2021-01-01'

        # set the variables
        var_cmd = f"set (now_date, from_date, last_order_date, last_order_x_month_ago, num_of_month_for_target) = "
        var_cmd += f"('{now_date}', '{from_date}', '{min_last_order_date}', {last_order_x_month_ago}, {num_of_month_for_target});"

        # set the query
        q = f"select * from {view_name}"

        if len(order_by) > 0:
            q += f" order by {order_by}"

        if limit > 0:
            q += f" limit {limit}"

        if offset > 0 and limit > 0:
            q += f" offset {offset}"

        q += ";"

        res = None

        try:
            # connect to snowflake
            con = sf_eng.connect()

            # execute the set vars command
            if len(ext_var_cmd) > 1:
                con.execute(ext_var_cmd)
            else:
                con.execute(var_cmd)

            # execute the query
            res = pd.read_sql_query(q, con)

            # change column names to uppercase
            res.columns = res.columns.str.upper()

        except Exception as e:
            print("Error!")
            print(str(e))

        finally:
            # close the connection
            con.close()
            sf_eng.dispose()

        return res

    def insert_to_sf(self, data_df, table_name, customer_name, password, replace=False):
        # get the snowflake engine object
        sf_eng = self.get_sf_con(customer_name, password)

        res = False

        i_if_exists = 'replace' if replace else 'append'

        try:
            # connect to snowflake
            con = sf_eng.connect()
            # insert the dataframe into snowflake
            data_df.to_sql(table_name, con=sf_eng, index=False,
                           if_exists=i_if_exists)  # make sure index is False, Snowflake doesnt accept indexes

            res = True

        except Exception as e:
            print("Error!")
            print(str(e))

        finally:
            # close the connection
            con.close()
            sf_eng.dispose()

        return res

    def insert_customer_cluster_ids(self, data_df, customer_name, password, replace=False):
        return self.insert_to_sf(data_df, 'CUSTOMER_TO_CLUSTER', customer_name, password, replace)

    def get_customer_dataset(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01',
                             min_last_order_date='2021-01-01', dataset_type='ALL'):
        # return get_data_from_sf('V1_SEPERATED_COL_NAMES', customer_name, password, now_date, from_date)

        base_view_name = 'V1_SEPERATED_COL_NAMES' if dataset_type == 'ALL' else 'V1_GET_CUSTOMER_TEST_SET'

        base_view_df = self.get_data_from_sf(base_view_name, customer_name, password, now_date, from_date,
                                             min_last_order_date)

        ext_str = ''

        if dataset_type == 'LAST_ORDER':
            ext_str = '_LAST_ORDER'

        if dataset_type == 'WITHOUT_LAST_ORDER':
            ext_str = '_WITHOUT_LAST_ORDER'

        product_pivot = f'V1_GET_PRODUCT_TOTAL_PER_CUSTOMER{ext_str}'
        product_type_pivot = f'V1_GET_PRODUCT_TYPE_TOTAL_PER_CUSTOMER{ext_str}'
        collection_pivot = f'V1_GET_COLLECTION_TOTAL_PER_CUSTOMER{ext_str}'

        # print(base_view_name)
        # print(product_pivot)
        # print(product_type_pivot)
        # print(collection_pivot)

        result = self.get_customer_dataset_with_dynamic_pivot(base_view_df, product_pivot, 'PRODUCT', customer_name,
                                                              password, now_date, from_date, min_last_order_date)
        result_wt = self.get_customer_dataset_with_dynamic_pivot(result, product_type_pivot, 'PRODUCT_TYPE', customer_name,
                                                                 password, now_date, from_date, min_last_order_date)
        result_wc = self.get_customer_dataset_with_dynamic_pivot(result_wt, collection_pivot, 'COLLECTION', customer_name,
                                                                 password, now_date, from_date, min_last_order_date)
        # return get_customer_dataset_with_dynamic_pivot(customer_name, password, now_date, from_date)
        return result_wc

    def get_customer_dataset_last_order(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01',
                                        min_last_order_date='2021-01-01'):
        return self.get_customer_dataset(customer_name, password, now_date, from_date, min_last_order_date, 'LAST_ORDER')

    def get_customer_dataset_without_last_order(self, customer_name, password, now_date='2021-01-01',
                                                from_date='2018-01-01', min_last_order_date='2021-01-01'):
        return self.get_customer_dataset(customer_name, password, now_date, from_date, min_last_order_date,
                                    'WITHOUT_LAST_ORDER')
    
    def get_customer_dataset_for_next_purchase(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01', 
                                               last_order_x_month_ago=3, num_of_month_for_target=3):
        return self.get_data_from_sf('V1_NEXT_PURCHASE_DATASET', customer_name, password, now_date, from_date, 
                                 last_order_x_month_ago=last_order_x_month_ago, num_of_month_for_target=num_of_month_for_target)

    def get_customer_dataset_for_next_purchase_with_last_order(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01', 
                                                               last_order_x_month_ago=3, num_of_month_for_target=3):
        return self.get_data_from_sf('V1_NEXT_PURCHASE_DATASET_FULL', customer_name, password, now_date, from_date, 
                                     last_order_x_month_ago=last_order_x_month_ago, num_of_month_for_target=num_of_month_for_target)
    
    def get_first_order_dataset_for_next_purchase(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01'):
        return self.get_data_from_sf('V1_NEXT_PURCHASE_DATASET_FIRST_ORDER', customer_name, password, now_date, from_date)

    def get_top_products(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01'):
        return self.get_data_from_sf('TBL_TOP_PRODUCTS', customer_name, password, now_date, from_date)

    def get_top_product_types(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01'):
        return self.get_data_from_sf('TBL_TOP_PRODUCT_TYPES', customer_name, password, now_date, from_date)

    def get_top_collections(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01'):
        return self.get_data_from_sf('TBL_TOP_COLLECTIONS', customer_name, password, now_date, from_date)
    
    def get_top_products_by_date(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01'):
        return self.get_data_from_sf('V1_GET_TOP_PRODUCTS_BY_DATE_RANKED', customer_name, password, now_date, from_date)

    def get_top_product_types_by_date(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01'):
        return self.get_data_from_sf('V1_GET_TOP_PRODUCT_TYPES_BY_DATE_RANKED', customer_name, password, now_date, from_date)

    def get_top_collections_by_date(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01'):
        return self.get_data_from_sf('V1_GET_TOP_COLLECTIONS_BY_DATE_RANKED', customer_name, password, now_date, from_date)

    def get_cluster_subtotal_and_avg_per_product_type(self, customer_name, password, now_date='2021-01-01',
                                                      from_date='2018-01-01'):
        return self.get_data_from_sf('V1_GET_CLUSTER_SPEND_PER_PRODUCT_TYPE', customer_name, password, now_date, from_date)

    def get_order_months(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01'):
        return self.get_data_from_sf('V1_GET_PURCHASE_MONTH', customer_name, password, now_date, from_date)
    
    def get_klaviyo_optin_emails(self, customer_name, password):
        return self.get_data_from_sf('V_KLAVIYO_OPTIN_EMAILS', customer_name, password)
    
    def get_customer_dataset_with_dynamic_pivot(self, base_df, pivot_view, pivot_on, customer_name, password,
                                                now_date='2021-01-01', from_date='2018-01-01',
                                                min_last_order_date='2021-01-01'):
        # base_df = get_data_from_sf('V1_SEPERATED_COL_NAMES', customer_name, password, now_date, from_date)
        # pre_pvt_df = get_data_from_sf('V1_GET_PRODUCT_TOTAL_PER_CUSTOMER', customer_name, password, now_date, from_date)
        pre_pvt_df = self.get_data_from_sf(pivot_view, customer_name, password, now_date, from_date, min_last_order_date)

        # print(len(pre_pvt_df))

        if len(pre_pvt_df) > 1:
            pivot_on = pivot_on.upper()

            base_df['CUSTOMER_ID'] = base_df['CUSTOMER_ID'].astype(str)
            pre_pvt_df['CUSTOMERID'] = pre_pvt_df['CUSTOMERID'].astype(str)

            pvt_df = pd.pivot_table(pre_pvt_df, values='SALE_QTY', index=['CUSTOMERID'],
                                    columns=[f'RANK_{pivot_on}_KEY'], aggfunc=np.sum)

            res_df = base_df.merge(pvt_df, how='outer', left_on='CUSTOMER_ID', right_on='CUSTOMERID')

            res_df.columns = res_df.columns.str.upper()

            return res_df[(res_df.CUSTOMER_ID != '0') & (res_df.CUSTOMER_ID.isna() == False)]
        else:
            return base_df

    def get_customer_dataset_agg_prodcut_type_per_order_by_cluster(self, customer_name, password, now_date='2021-01-01',
                                                                   from_date='2018-01-01'):
        pivot_on = 'PRODUCT_TYPE'
        pivot_view = 'GET_PRODUCT_TYPE_TOTAL_PER_CUSTOMER_ORDER_BY_CLUSTER'

        base_df = self.get_data_from_sf('V1_SEPERATED_COL_NAMES_PER_CUSTOMER_ORDER_BY_CLUSTER', customer_name, password,
                                        now_date, from_date)
        pre_pvt_df = self.get_data_from_sf(pivot_view, customer_name, password, now_date, from_date)

        prod_type_df = self.get_data_from_sf('TBL_TOP_PRODUCT_TYPES', customer_name, password, now_date)

        if len(pre_pvt_df) > 1:
            pivot_on = pivot_on.upper()

            base_df['CUSTOMER_ID'] = base_df['CUSTOMER_ID'].astype(str)
            pre_pvt_df['CUSTOMERID'] = pre_pvt_df['CUSTOMERID'].astype(str)

            pvt_df = pd.pivot_table(pre_pvt_df, values='SALE_QTY', index=['CUSTOMERID'],
                                    columns=[f'RANK_{pivot_on}_KEY'], aggfunc=np.sum)

            res_df = base_df.merge(pvt_df, how='outer', left_on='CUSTOMER_ID', right_on='CUSTOMERID')

            res_df.columns = res_df.columns.str.upper()

            return res_df[(res_df.CUSTOMER_ID != '0') & (res_df.CUSTOMER_ID.isna() == False)]
        else:
            return base_df

    def grant_permissions(self, customer_name, password, obj_type, role_name='', grant_on_future_objects=0):
        grant_on = 'future' if grant_on_future_objects == 1 else 'all'
        grant_cmd = f'grant select on {grant_on} {obj_type} in SCHEMA "{customer_name}"."PUBLIC" to role {role_name};'

        return self.exec_sf(grant_cmd, customer_name, password, role_name)

    def grant_permissions_on_tables_to_accountadmin(self, customer_name, password, grant_on_future_objects=0):
        return self.grant_permissions(customer_name, password, 'tables', 'ACCOUNTADMIN', grant_on_future_objects)

    def grant_permissions_on_views_to_accountadmin(self, customer_name, password, grant_on_future_objects=0):
        return self.grant_permissions(customer_name, password, 'views', 'ACCOUNTADMIN', grant_on_future_objects)

    def get_demand_prediction_dataset(self, customer_name, password, now_date='2021-01-01', num_of_month_to_agg_by=12, 
                                      num_of_items_to_agg_by=1000):
        ext_var_cmd = f"set (now_date, num_of_month_to_agg_by, num_of_items_to_agg_by) = ('{now_date}', '{num_of_month_to_agg_by}', '{num_of_items_to_agg_by}');"

        return self.get_data_from_sf('V1_DEMAND_PREDICTION', customer_name, password, ext_var_cmd = ext_var_cmd)

    def get_demand_prediction_daily_dataset(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01'):
        return self.get_data_from_sf('V1_DEMAND_PREDICTION_DAILY', customer_name, password, now_date, from_date)

    def set_top_tables(self, customer_name, password, table_date=''):
        res = []

        name_suffix = f'_{table_date}' if len(table_date) > 1 else ''

        top_collections = f"""
        create or replace table TBL_TOP_COLLECTIONS{name_suffix}
        as
        SELECT * FROM V1_GET_TOP_COLLECTIONS
        ORDER BY rank;
        """

        top_product_types = f"""
        create or replace table TBL_TOP_PRODUCT_TYPES{name_suffix}
        as
        SELECT * FROM V1_GET_TOP_PRODUCT_TYPES
        ORDER BY rank;
        """

        top_products = f"""
        create or replace table TBL_TOP_PRODUCTS{name_suffix}
        as
        SELECT * FROM V1_GET_TOP_PRODUCTS
        ORDER BY rank;
        """

        print(top_collections)
        print(top_product_types)
        print(top_products)

        res.append(self.exec_sf(top_collections, customer_name, password))
        res.append(self.exec_sf(top_product_types, customer_name, password))
        res.append(self.exec_sf(top_products, customer_name, password))

        return all(res)

    def get_data_from_sf_for_clv(self, view_name, customer_name, password, now_date='2021-01-01', from_date='2018-01-01', num_of_month=3, target_num_of_month=14):
        # get the snowflake engine object
        sf_eng = self.get_sf_con(customer_name, password)

        # validate variables
        if not self.is_valid_date(now_date):
            now_date = '2021-01-01'

        if not self.is_valid_date(from_date):
            from_date = '2018-01-01'

        # set the variables
        var_cmd = f"set (now_date, from_date, num_of_month, target_num_of_month) = "
        var_cmd += f"('{now_date}', '{from_date}', {num_of_month}, {target_num_of_month});"

        # set the query
        q = f"select * from {view_name};"

        res = None

        try:
            # connect to snowflake
            con = sf_eng.connect()

            # execute the set vars command
            con.execute(var_cmd)

            # execute the query
            res = pd.read_sql_query(q, con)

            # change column names to uppercase
            res.columns = res.columns.str.upper()

        except Exception as e:
            print("Error!")
            print(str(e))

        finally:
            # close the connection
            con.close()
            sf_eng.dispose()

        return res

    def get_customer_clv_dataset_with_dynamic_pivot(self, base_df, pivot_view, pivot_on, customer_name, password, now_date='2021-01-01', from_date='2018-01-01'):    
        pre_pvt_df = self.get_data_from_sf(pivot_view, customer_name, password, now_date, from_date)

        if len(pre_pvt_df) > 1:
            pivot_on = pivot_on.upper()

            base_df['CUSTOMER_ID'] = base_df['CUSTOMER_ID'].astype(str)
            pre_pvt_df['CUSTOMERID'] = pre_pvt_df['CUSTOMERID'].astype(str)

            pvt_df = pd.pivot_table(pre_pvt_df, values='SALE_QTY', index=['CUSTOMERID'], columns=[f'RANK_{pivot_on}_KEY'], aggfunc=np.sum)

            res_df = base_df.merge(pvt_df, how='outer', left_on='CUSTOMER_ID', right_on='CUSTOMERID')

            res_df.columns = res_df.columns.str.upper()

            return res_df[(res_df.CUSTOMER_ID != '0') & (res_df.CUSTOMER_ID.isna() == False)]
        else:
            return base_df

    def get_customer_clv_dataset(self, customer_name, password, now_date='2021-01-01', from_date='2018-01-01', model_type=1, num_of_month=3, target_num_of_month=14):
        #return get_data_from_sf('V1_SEPERATED_COL_NAMES', customer_name, password, now_date, from_date)

        base_view_name = f'V_CLV_DATASET_MODEL_{model_type}' 

        base_view_df = self.get_data_from_sf_for_clv(base_view_name, customer_name, password, now_date, from_date, num_of_month, target_num_of_month)

        return base_view_df
        #product_pivot_total = f'V_GET_PRODUCT_TOTAL_PER_CUSTOMER_MODEL_{model_type}'
        #product_pivot_avg = f'V_GET_PRODUCT_AVG_PER_CUSTOMER_MODEL_{model_type}'
        #collection_pivot_total = f'V_GET_COLLECTION_TOTAL_PER_CUSTOMER_MODEL_{model_type}'
        #collection_pivot_avg = f'V_GET_COLLECTION_AVG_PER_CUSTOMER_MODEL_{model_type}'


        #result = self.get_customer_clv_dataset_with_dynamic_pivot(base_view_df, product_pivot_total, 'PRODUCT', customer_name, password, now_date, from_date)
        #result_w_avg = self.get_customer_clv_dataset_with_dynamic_pivot(result, product_pivot_avg, 'PRODUCT', customer_name, password, now_date, from_date)

        #result_wc = self.get_customer_clv_dataset_with_dynamic_pivot(result_w_avg, collection_pivot_total, 'COLLECTION', customer_name, password, now_date, from_date)
        #result_wc_avg = self.get_customer_clv_dataset_with_dynamic_pivot(result_wc, collection_pivot_avg, 'COLLECTION', customer_name, password, now_date, from_date)
        # return get_customer_dataset_with_dynamic_pivot(customer_name, password, now_date, from_date)
        #return result_wc_avg
