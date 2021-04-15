#%%
from datetime import datetime, timedelta, timezone
from google.cloud import bigquery, storage
from google.cloud.exceptions import NotFound
from google.cloud.bigquery import ExtractJobConfig, TimePartitioning, RangePartitioning, PartitionRange
from utils.commons import timestamp_chunk
import json

# %% For local
import google.auth
import os
HOME = os.getcwd()
CLIENT_ID = 'contxtsio-nftbank'
CREDENTIALS = f"./.cred/pipeline-executor.contxtsio-nftbank.credentials"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS

SCOPE = ('https://www.googleapis.com/auth/bigquery',
         'https://www.googleapis.com/auth/cloud-platform',
         'https://www.googleapis.com/auth/drive')
credentials, _ = google.auth.default(scopes=SCOPE)

bq_client = bigquery.Client(CLIENT_ID, credentials=credentials)
storage_client = storage.Client(CLIENT_ID, credentials=credentials)

# %%
def _does_data_ready(data_name, date_path):
    blob_list = storage_client.list_blobs("nftbank-matic-network", max_results=24, prefix=f"export/raw/{data_name}/block_date={date_path}")
    blobs = [blob for blob in blob_list]

    return len(blobs) == 24

# %%
def _does_table_exist(dataset_id, table_name):
    dataset = bq_client.dataset(dataset_id, project="contxtsio-nftbank")
    table_ref = dataset.table(table_name)
    try:
        bq_client.get_table(table_ref)
        return True
    except NotFound:
        return False

# %%
def load_table(data_name, block_date):

    date_path = block_date.strftime("%Y-%m-%d")
    date_suffix = block_date.strftime('%Y%m%d')

    if not _does_data_ready(data_name, date_path):
        print("Dependency dataset are not ready. Skip staging job.")
        return None

    if _does_table_exist("matic_staging_area", f"raw_{data_name}_{date_suffix}"):
        print("Already exists. Skip staging jobs.")
        return None

    schema_dicts = json.load(open(f"./schema/raw/{data_name}.json", "r+"))
    schema = [bigquery.SchemaField.from_api_repr(schema_dict) for schema_dict in schema_dicts]

    # Load bq data
    job_config = bigquery.LoadJobConfig()
    hive_partitioning = bigquery.external_config.HivePartitioningOptions()
    hive_partitioning.mode = "CUSTOM"
    hive_partitioning.source_uri_prefix = f"gs://nftbank-matic-network/export/raw/{data_name}/block_date={date_path}/{{block_hour:STRING}}/"  #path to hive partition data
    job_config.hive_partitioning = hive_partitioning

    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job_config.schema = schema
    # job_config.time_partitioning = bigquery.TimePartitioning(type_=bigquery.TimePartitioningType().DAY, field='block_date')
    job_config.autodetect = True

    # # full
    # uri = "gs://nftbank-metadata/discord/users/*.jsonl"  #path to data

    # incr
    src = f"gs://nftbank-matic-network/export/raw/{data_name}/block_date={date_path}/*.json"  #path to data
    dst = f"contxtsio-nftbank.matic_staging_area.raw_{data_name}_{date_suffix}"

    load_job = bq_client.load_table_from_uri(src, dst, job_config=job_config)  # API request

    print(f"load {src} to {dst}")

    return load_job.result()  # Waits for table load to complete.

# %%
def enrich_table(data_name, block_date, partition_field, mode='append', if_exists='ignore'):
    date_path = block_date.strftime("%Y-%m-%d")
    date_suffix = block_date.strftime('%Y%m%d')

    if not _does_table_exist("matic_staging_area", f"raw_blocks_{date_suffix}"):
        print("Dependency tables are not ready. Skip enriching job.")
        return None
    if not _does_table_exist("matic_staging_area", f"raw_transactions_{date_suffix}"):
        print("Dependency tables are not ready. Skip enriching job.")
        return None
    if not _does_table_exist("matic_staging_area", f"raw_receipts_{date_suffix}"):
        print("Dependency tables are not ready. Skip enriching job.")
        return None
    if not _does_table_exist("matic_staging_area", f"raw_logs_{date_suffix}"):
        print("Dependency tables are not ready. Skip enriching job.")
        return None

    sql = (open(f"./sqls/{data_name}.bqsql", "r+").read()).format(date_path=date_path, date_suffix=date_suffix)

    try:
        existing = bq_client.query(f"""
            select count(*) as row_count from `contxtsio-nftbank.matic_staging_area.{data_name}` where date({partition_field}) = "{date_path}";
            """, location='US', retry=bigquery.DEFAULT_RETRY.with_deadline(900)).result()

        existing_count = [dict(row) for row in existing][0]['row_count']
    except:
        existing_count = 0

    if if_exists == 'ignore' and existing_count > 0:
        print(f"Already exists ({existing_count} rows). Skip enriching job.")
        # TODO:
        return None
    else:
        # Set the destination table
        job_config = bigquery.QueryJobConfig()

        table_ref = bq_client.dataset("matic_staging_area").table(data_name)
        job_config.destination = table_ref
        if mode == 'overwrite':
            job_config.write_disposition = 'WRITE_TRUNCATE'
        else:
            job_config.write_disposition = 'WRITE_APPEND'
        print('create table `{}.{}.{}`'.format("contxtsio-nftbank", "matic_staging_area", data_name))
        job_config.time_partitioning = bigquery.TimePartitioning(field=partition_field)

        query_job = bq_client.query(
            sql, location='US',
            retry=bigquery.DEFAULT_RETRY.with_deadline(900),
            job_config=job_config)  # API request - starts the query

        return query_job.result()  # Waits for the query to finish


# %%
start = datetime(2021,2,27, tzinfo=timezone.utc)
end = datetime(2021,3,2, tzinfo=timezone.utc) + timedelta(minutes=5)


# %%
for from_timestamp, to_timestamp in timestamp_chunk(start, end, interval=timedelta(days=1)):
    print("==============================================")
    print(f"""
    stage and enrich
    FROM: {from_timestamp}
    TO  : {to_timestamp}
    """)
    load_table('blocks', from_timestamp)
    load_table('transactions', from_timestamp)
    load_table('logs', from_timestamp)
    load_table('receipts', from_timestamp)

    enrich_table('blocks', from_timestamp, partition_field='timestamp')
    enrich_table('transactions', from_timestamp, partition_field='block_timestamp')
    enrich_table('logs', from_timestamp, partition_field='block_timestamp')
    print("\n==============================================")
# %%
