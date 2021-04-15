import boto3
import os
import pandas as pd
import time

from boto3.dynamodb.conditions import Key, Attr
from boto3.session import Session
from botocore.exceptions import ClientError
from datetime import datetime
from decimal import Decimal
from hashlib import md5
from datupapi.configure.config import Config
from sqlalchemy import create_engine


class IO(Config):

    def __init__(self, config_file, logfile, log_path, *args, **kwargs):
        Config.__init__(self, config_file=config_file, logfile=logfile)
        self.log_path = log_path


    def download_mssql(self, hostname, db_user, db_passwd, db_name, port, table_name):
        """Return a dataframe containing the data extracted from MSSQL database's table supporting PyODBC connector

        :param hostname: Public IP address or hostname of the remote database server
        :param db_user: Username of the database
        :param db_passwd: Password of the database
        :param db_name: Name of the target database
        :param port: TCP port number of the database (usually 1433)
        :param table_name: Name of target table
        :return df: Dataframe containing the data from database's table

        >>> df = extract_mssql(hostname='202.10.0.1', db_user='johndoe', db_passwd='123456', db_name='dbo.TheDataBase')
        >>> df
              var1    var2    var3
        idx0     1       2       3
        """
        engine = create_engine('mssql+pymssql://' + db_user + ':' + db_passwd + '@' + hostname + ':' + port + '/' + db_name)
        try:
            connection = engine.connect()
            stmt = 'SELECT TOP 10 * FROM ' + table_name
            results = connection.execute(stmt).fetchall()
            df = pd.DataFrame(results)
            df.columns = results[0].keys()
        except ConnectionRefusedError as err:
            logger.exception(f'Refused connection to the database. Please check parameters: {err}')
            raise
        return df


    def download_csv(self, q_name, datalake_path=None, sep=',', index_col=None, squeeze=False, num_records=None, dayfirst=False, compression='infer', encoding='utf-8', low_memory=True, types=None):
        """Return a dataframe from a csv file stored in the datalake

        :param q_name: Plain file (.csv) to download and stored in a dataframe
        :param datalake_path: Path to download the file from the S3 datalake. Default None.
        :param sep: Field delimiter of the downloaded file. Default ','
        :param index_col: Column(s) to use as the row labels of the DataFrame, either given as string name or column index.
        :param squeeze: If the parsed data only contains one column then return a Series. Default False
        :param num_records: Number of records to fetch from the source. Default None
        :param dayfirst: DD/MM format dates, international and European format. Default False
        :param compression: For on-the-fly decompression of on-disk data. Default 'infer'
        :param encoding: Encoding to use for UTF when reading/writing. Default 'utf-8'
        :param low_memory: Internally process the file in chunks, resulting in lower memory use while parsing, but possibly mixed type inference. Default True
        :param types: Dict with data columns as keys and data types as values. Default None
        :return df: Dataframe containing the data from the file stored in the datalake

        >>> df = download_csv(q_name='Q', datalake_path='as-is/folder')
        >>> df
              var1    var2    var3
        idx0     1       2       3
        """
        s3_client = boto3.client('s3', region_name=self.region, aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        file_path = os.path.join(Config.LOCAL_PATH, q_name + '.csv')
        try:
            if datalake_path is None:
                s3_client.download_file(self.datalake, q_name + '.csv', file_path)
            else:
                s3_client.download_file(self.datalake, os.path.join(datalake_path, q_name, q_name + '.csv'), file_path)
            df = pd.read_csv(file_path,
                             sep=sep,
                             index_col=index_col,
                             squeeze=squeeze,
                             nrows=num_records,
                             dayfirst=dayfirst,
                             compression=compression,
                             encoding=encoding,
                             low_memory=low_memory,
                             dtype=types)
        except ClientError as err:
            self.logger.exception(f'No connection to the datalake. Please check the paths: {err}')
        except FileNotFoundError as err:
            self.logger.exception(f'No csv file found. Please check paths: {err}')
            raise
        return df


    def download_object_csv(self, datalake_path=None, sep=',', index_col=None, squeeze=False, num_records=None, dayfirst=False, compression='infer', encoding='utf-8', low_memory=True, types=None):
        """Return a dataframe from a file stored in the datalake

        :param datalake_path: Path to download the file from the S3 datalake. Do not include datalake name. Default None.
        :param sep: Field delimiter of the downloaded file. Default ','
        :param index_col: Column(s) to use as the row labels of the DataFrame, either given as string name or column index.
        :param squeeze: If the parsed data only contains one column then return a Series. Default False
        :param num_records: Number of records to fetch from the source. Default None
        :param dayfirst: DD/MM format dates, international and European format. Default False
        :param compression: For on-the-fly decompression of on-disk data. Default 'infer'
        :param encoding: Encoding to use for UTF when reading/writing. Default 'utf-8'
        :param low_memory: Internally process the file in chunks, resulting in lower memory use while parsing, but possibly mixed type inference. Default True
        :param types: Dict with data columns as keys and data types as values. Default None
        :return df: Dataframe containing the data from the file stored in the datalake

        >>> df = download_csv(datalake_path='as-is/folder/file')
        >>> df
              var1    var2    var3
        idx0     1       2       3
        """
        s3_client = boto3.client('s3',
                                 region_name=self.region,
                                 aws_access_key_id=self.access_key,
                                 aws_secret_access_key=self.secret_key)
        file_path = os.path.join(Config.LOCAL_PATH, 'object.dat')
        try:
            s3_client.download_file(self.datalake, os.path.join(datalake_path), file_path)
            df = pd.read_csv(file_path,
                             sep=sep,
                             index_col=index_col,
                             squeeze=squeeze,
                             nrows=num_records,
                             dayfirst=dayfirst,
                             compression=compression,
                             encoding=encoding,
                             low_memory=low_memory,
                             dtype=types)
        except ClientError as err:
            self.logger.exception(f'No connection to the datalake. Please check the paths: {err}')
        except FileNotFoundError as err:
            self.logger.exception(f'No object file found. Please check paths: {err}')
            raise
        return df


    def download_all_objects_csv(self, datalake_path=None, sep=',', index_col=None, squeeze=False, num_records=None, dayfirst=False, compression='infer', encoding='utf-8', low_memory=True, types=None):
        """Return a dataframe from a file stored in the datalake

        :param datalake_path: Path to download the file from the S3 datalake. Do not include datalake name. Default None.
        :param sep: Field delimiter of the downloaded file. Default ','
        :param index_col: Column(s) to use as the row labels of the DataFrame, either given as string name or column index.
        :param squeeze: If the parsed data only contains one column then return a Series. Default False
        :param num_records: Number of records to fetch from the source. Default None
        :param dayfirst: DD/MM format dates, international and European format. Default False
        :param compression: For on-the-fly decompression of on-disk data. Default 'infer'
        :param encoding: Encoding to use for UTF when reading/writing. Default 'utf-8'
        :param low_memory: Internally process the file in chunks, resulting in lower memory use while parsing, but possibly mixed type inference. Default True
        :param types: Dict with data columns as keys and data types as values. Default None
        :return df: Dataframe containing the data from the file stored in the datalake

        >>> df = download_csv(datalake_path='as-is/folder/file')
        >>> df
              var1    var2    var3
        idx0     1       2       3
        """
        s3_resource = boto3.resource('s3',
                                     region_name=self.region,
                                     aws_access_key_id=self.access_key,
                                     aws_secret_access_key=self.secret_key)

        try:
            df = pd.DataFrame()
            datalake = s3_resource.Bucket(self.datalake)
            objects = datalake.objects.filter(Prefix=datalake_path)
            for obj in objects:
                path, filename = os.path.split(obj.key)
                if filename != '_SUCCESS' and filename != '_CHECK':
                    datalake.download_file(obj.key, os.path.join('/tmp', filename))
                    df_tmp = pd.read_csv(os.path.join('/tmp', filename),
                                         sep=sep,
                                         index_col=index_col,
                                         squeeze=squeeze,
                                         nrows=num_records,
                                         dayfirst=dayfirst,
                                         compression=compression,
                                         encoding=encoding,
                                         low_memory=low_memory,
                                         dtype=types)
                    df = pd.concat([df, df_tmp], axis='rows')
        except ClientError as err:
            self.logger.exception(f'No connection to the datalake. Please check the paths: {err}')
        except FileNotFoundError as err:
            self.logger.exception(f'No object file found. Please check paths: {err}')
            raise
        return df


    def download_dynamodb(self, table_name, tenant_id):
        """
        Return a dataframe with the data fetch from DynamoDB

        :param table_name: Table name in DynamoDB table
        :param tenant_id: Partition column mapping tenant's ID to whom belongs the records
        :return df: Dataframe to store records fetched from DynamoDB
        >>> df = download_dynamodb(table_name='sampleTbl', tenant_id='1234')
        >>> df =
                tenantId    Date         Attr
        idx0    A121        2020-12-01   3
        """
        dydb_client = boto3.client('dynamodb', region_name=self.region, aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        dynamodb_session = Session(aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key, region_name=self.region)
        dydb = dynamodb_session.resource('dynamodb')
        try:
            dynamo_tbl = dydb.Table(table_name)
            response = dynamo_tbl.query(
                KeyConditionExpression=Key('tenantId').eq(md5(tenant_id.encode('utf-8')).hexdigest()) &\
                                       Key('Fecha').between('2010-01-01', '2025-12-31')
            )
            items = response['Items']
        except dydb_client.exceptions.ResourceNotFoundException as err:
            print(f'Table not found. Please check names :{err}')
            return False
            raise
        return items


    def download_excel(self, q_name, sheet_name, datalake_path=None, index_col=None, squeeze=False, num_records=None, types=None, header_=0, skiprows_=None):
        """Return a dataframe from a csv file stored in the datalake

        :param q_name: Excel file to download and stored in a dataframe. Include extension xls, xlsx, ods, etc.
        :param sheet_name: Excel sheet to download and stored in a dataframe
        :param datalake_path: Path to download the file from the S3 datalake. Default None.
        :param index_col: Column(s) to use as the row labels of the DataFrame, either given as string name or column index.
        :param squeeze: If the parsed data only contains one column then return a Series. Default False
        :param num_records: Number of records to fetch from the source. Default None
        :param types: Dict with data columns as keys and data types as values. Default None
        :return df: Dataframe containing the data from the file stored in the datalake

        >>> df = download_excel(q_name='Q', sheet_name='sheet1', datalake_path='as-is/folder')
        >>> df
              var1    var2    var3
        idx0     1       2       3
        """
        s3_client = boto3.client('s3', region_name=self.region, aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        file_path = os.path.join(Config.LOCAL_PATH, q_name)
        try:
            if datalake_path is None:
                s3_client.download_file(self.datalake, q_name, file_path)
            else:
                s3_client.download_file(self.datalake, os.path.join(datalake_path, q_name), file_path)
            df = pd.read_excel(file_path, sheet_name=sheet_name, index_col=index_col, squeeze=squeeze, engine='openpyxl', nrows=num_records, dtype=types, header=header_, skiprows=skiprows_)
            df = df.dropna(how='all')
        except ClientError as err:
            self.logger.exception(f'No connection to the datalake. Please check the paths: {err}')
        except FileNotFoundError as err:
            self.logger.exception(f'No excel file or sheet name found. Please check paths: {err}')
            raise
        return df


    def upload_csv(self, df, q_name, datalake_path, sep=',', encoding='utf-8', date_format='%Y-%m-%d'):
        """Return a success or failure boolean attempting to upload a local file to the datalake

        :param df: Dataframe to upload
        :param q_name: File name to save dataframe
        :param datalake_path: Path to upload the Q to S3 datalake
        :param sep: Field delimiter for the output file. Default ','
        :param date_format: Format string for datetime objects of output file. Default '%Y-%m-%d'
        :param encoding: A string representing the encoding to use in the output file. Default 'utf-8'
        :return: True if success, else False.

        >>> upload_csv(df=df, q_name='Q', datalake_path='as-is/folder')
        >>> True
        """
        file_path = os.path.join(Config.LOCAL_PATH, q_name + '.csv')
        df.to_csv(file_path, sep=sep, encoding=encoding, date_format=date_format, index=False)
        s3_client = boto3.client('s3', region_name=self.region, aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        try:
            response = s3_client.upload_file(file_path, self.datalake, os.path.join(datalake_path, q_name, q_name + '.csv'))
        except ClientError as err:
            self.logger.exception(f'No connection to the datalake. Please check the paths: {err}')
            return False
        except FileNotFoundError as err:
            self.logger.exception(f'No excel file or sheet name found. Please check paths: {err}')
            return False
        return True


    def upload_dynamodb(self, df, table_name, tenant_id, sort_col):
        """
        Return a success or failure boolean attempting to upload timeseries data to DynamoDB

        :param df: Dataframe to upload to DynamoDB table
        :param table_name: Table name in DynamoDB table
        :param tenant_id: Partition column mapping tenant's ID to whom belongs the records
        :param sort_col: Sorting column mapping usually to date column
        :return response: HTTP status code response. If 400 success, failure otherwise

        >>> upload_dynamodb(df=df, table_name=sampleTbl, tenant_id='acme', sort_col='Date')
        >>> True
        """
        dydb_client = boto3.client('dynamodb', region_name=self.region, aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        dynamodb_session = Session(aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key, region_name=self.region)
        dydb = dynamodb_session.resource('dynamodb')
        try:
            dynamo_tbl = dydb.Table(table_name)
            with dynamo_tbl.batch_writer() as batch:
                for row in df.itertuples(index=False):
                    record = {}
                    record.update({'tenantId': md5(tenant_id.encode('utf-8')).hexdigest()})
                    record.update({sort_col: row[0].strftime('%Y-%m-%d')})
                    for ix, rec in enumerate(row[1:]):
                        record.update({df.columns[ix + 1]: Decimal(str(rec))})
                    batch.put_item(Item=record)
        except dydb_client.exceptions.ResourceNotFoundException as err:
            print(f'Table not found. Please check names :{err}')
            return False
            raise
        return True


    def upload_timestream(self, df, db_name, table_name):
        """
        Return a success or failure boolean attempting to upload timeseries data to timestream database

        :param df: Dataframe to upload to Timestream table
        :param db_name: Database name in Timestream service
        :param table_name: Table name in Timestream service
        :return response: HTTP status code response. If 400 success, failure otherwise

        >>> upload_timestream(df=df, db_name=dbSample, table_name=tbSample)
        >>> True
        """
        ts_client = boto3.client('timestream-write', region_name=self.region, aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        dimensions = [
            {'Name': 'tenantId', 'Value': '1000', 'DimensionValueType': 'VARCHAR'}
        ]
        records = []
        for row in df.itertuples(index=False):
            for ix, rec in enumerate(row[1:]):
                records.append({
                    'Dimensions': dimensions,
                    'MeasureName': df.columns[ix + 1],
                    'MeasureValue': str(rec),
                    'MeasureValueType': 'DOUBLE',
                    'Time': str(int(pd.to_datetime(row[0]).timestamp())),
                    'TimeUnit': 'SECONDS',
                    'Version': 3
                })
        try:
            response = ts_client.write_records(DatabaseName=db_name,
                                               TableName=table_name,
                                               Records=records)
            status = response['ResponseMetadata']['HTTPStatusCode']
            print(f'Processed records: {len(records)}. WriteRecords status: {status}')
            self.logger.exception(f'Processed records: {len(records)}. WriteRecords status: {status}')
        except ts_client.exceptions.RejectedRecordsException as err:
            print(f'{err}')
            self.logger.exception(f'{err}')
            for e in err.response["RejectedRecords"]:
                print("Rejected Index " + str(e["RecordIndex"]) + ": " + e["Reason"])
                self.logger.exception("Rejected Index " + str(e["RecordIndex"]) + ": " + e["Reason"])
            return False
        except ts_client.exceptions.ValidationException as err:
            print(f"{err.response['Error']['Message']}")
            self.logger.exception(f"{err.response['Error']['Message']}")
            return False
        return status


    def upload_log(self):
        """Return a success or failure boolean attempting to upload a local file to the datalake

        :param datalake_path: Path to upload the Q to S3 datalake
        :return: True if success, else False.

        >>> upload_log()
        >>> True
        """
        file_path = os.path.join(Config.LOCAL_PATH, self.logfile)
        s3_client = boto3.client('s3', region_name='us-east-1', aws_access_key_id=self.access_key,
                                 aws_secret_access_key=self.secret_key)
        try:
            response = s3_client.upload_file(file_path, self.datalake, os.path.join(self.log_path, self.logfile))
        except ClientError as err:
            self.logger.exception(f'No connection to the datalake. Please check the paths: {err}')
            return False
        except FileNotFoundError as err:
            self.logger.exception(f'No excel file or sheet name found. Please check paths: {err}')
            return False
        return True