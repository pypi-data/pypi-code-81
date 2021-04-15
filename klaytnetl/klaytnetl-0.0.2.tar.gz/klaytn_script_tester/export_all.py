# # %%
# # Append parent package (DEV)
# import os, sys
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


# %%
import logging


# %%
from klaytnetl.cli import (
    get_block_range_for_timestamps,
    export_enrich_block_group
)
import os


# %%
from datetime import datetime, timedelta, timezone
from tempfile import TemporaryDirectory
from typing import List, Union, Iterator


# %%
from utils.commons import timestamp_chunk
from utils.google_cloud_storage_hook import SimpleGoogleCloudStorageHook
from utils.task_manager import TaskManager, TaskIDs

# %%
import google.auth
import google.oauth2.service_account


# %%
# API_SERVICE = "kas"
# PROVIDER_URI = "https://node-api.klaytnapi.com/v1/klaytn"
# AUTH_ID = "KASKKB3WG1PRS40GTWPY54QZ"
# AUTH_SECRET = "kwmEkAKbQp8sRJ6N2OxPHJcrVoGr8TgTQaTh4sPv"
# X_CHAIN_ID = "8217"

# export_max_workers = 20
# export_batch_size = 1
# output_bucket = "nftbank-klaytn-network"

# %%
API_SERVICE = "web3"
PROVIDER_URI = "http://35.188.61.188:8551"
AUTH_ID = None
AUTH_SECRET = None
X_CHAIN_ID = None

export_max_workers = 10
export_batch_size = 20
output_bucket = "nftbank-klaytn-network"

# %%
CREDENTIALS = f".cred/pipeline-executor.contxtsio-nftbank.credentials"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS
SCOPE = ('https://www.googleapis.com/auth/cloud-platform',
        # 'https://www.googleapis.com/auth/bigquery',
        # 'https://www.googleapis.com/auth/drive'
        )
credentials, _ = google.auth.default(scopes=SCOPE)

cloud_storage_hook = SimpleGoogleCloudStorageHook(credentials=credentials, project_id="contxtsio-nftbank")

# %%
task_manager = TaskManager(mongodb_connection_uri="mongodb+srv://masterContxtsio:Contxtsio!23@cluster0.7qjx5.mongodb.net/admin?retryWrites=true&w=majority",
                           min_timestamp=datetime(2020, 6, 17, 0, 0, 0, 0, tzinfo=timezone.utc))
task_manager.initialize_db(TaskIDs['ALL'], "raw")

# %%
# Export
def export_path(directory, start_timestamp):
    return "export/raw/{directory}/block_date={block_date}/block_hour={block_hour}/".format(
        directory=directory,
        block_date=start_timestamp.strftime("%Y-%m-%d"),
        block_hour=start_timestamp.strftime("%H"),
    )

def copy_to_export_path(file_path, export_path):
    logging.info('Calling copy_to_export_path({}, {})'.format(file_path, export_path))
    filename = os.path.basename(file_path)

    cloud_storage_hook.upload_to_gcs(
        gcs_hook=cloud_storage_hook,
        bucket=output_bucket,
        object=export_path + filename,
        filename=file_path)

def copy_from_export_path(export_path, file_path):
    logging.info('Calling copy_from_export_path({}, {})'.format(export_path, file_path))
    filename = os.path.basename(file_path)

    cloud_storage_hook.download_from_gcs(gcs_hook=cloud_storage_hook, bucket=output_bucket, object=export_path + filename, filename=file_path)


# %%
storage_client = cloud_storage_hook.get_conn()

# %%
def add_provider_uri_fallback_loop(python_callable, provider_uris):
    """Tries each provider uri in provider_uris until the command succeeds"""

    def python_callable_with_fallback(**kwargs):
        for index, provider_uri in enumerate(provider_uris):
            kwargs['provider_uri'] = provider_uri
            try:
                ret = python_callable(**kwargs)
                break
            except Exception as e:
                if index < (len(provider_uris) - 1):
                    logging.exception('An exception occurred. Trying another uri')
                else:
                    raise e

        return ret

    return python_callable_with_fallback

# %%
##########################################
### EXTRANCTIONS
##########################################

# %%
def _get_block_range(provider_uri, start_timestamp, end_timestamp, **kwargs):
    with TemporaryDirectory() as tempdir:
        logging.info('Calling get_block_range_for_timestamps ({}, {})'.format(start_timestamp, end_timestamp))
        get_block_range_for_timestamps.callback(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            output=os.path.join(tempdir, "blocks_meta.txt"),
            provider_uri=provider_uri,
            **kwargs
        )

        with open(os.path.join(tempdir, "blocks_meta.txt")) as block_range_file:
            block_range = block_range_file.read()
            start_block, end_block = block_range.split(",")

    return int(start_block), int(end_block)


# %%
def _export_enrich_block_group_command(start_timestamp, start_block, end_block, provider_uri, max_workers, batch_size, file_format, file_maxlines, compress, **kwargs):
    with TemporaryDirectory() as tempdir:
        logging.info('Calling export_enrich_block_group ({}, {})'.format(start_block, end_block))

        export_enrich_block_group.callback(
            start_block=start_block,
            end_block=end_block,
            provider_uri=provider_uri,
            blocks_output=os.path.join(tempdir, "blocks.json"),
            transactions_output=os.path.join(tempdir, "transactions.json"),
            logs_output=os.path.join(tempdir, "logs.json"),
            token_transfers_output=os.path.join(tempdir, "token_transfers.json"),
            max_workers=max_workers,
            batch_size=batch_size,
            file_format=file_format,
            file_maxlines=file_maxlines,
            compress=compress,
            **kwargs
        )

        copy_to_export_path(
                os.path.join(tempdir, "blocks.json"), export_path("blocks", start_timestamp)
        )

        copy_to_export_path(
            os.path.join(tempdir, "transactions.json"), export_path("transactions", start_timestamp)
        )

        copy_to_export_path(
                os.path.join(tempdir, "logs.json"), export_path("logs", start_timestamp)
        )

        copy_to_export_path(
            os.path.join(tempdir, "token_transfers.json"), export_path("token_transfers", start_timestamp)
        )


# %%
##########################################
### Get target ranges
##########################################
for task in task_manager.get_todos(TaskIDs["ALL"], "raw"):
    start_timestamp = task['start_timestamp']
    end_timestamp = task['end_timestamp']
    print(start_timestamp, end_timestamp)

    task_manager.task_started(TaskIDs["ALL"], "raw", start_timestamp, end_timestamp)

    ##########################################
    ### Get start / end block number
    ##########################################
    get_block_range = add_provider_uri_fallback_loop(
        _get_block_range,
        provider_uris=[PROVIDER_URI],
        )
    start_block, end_block = get_block_range(**{
        "start_timestamp": start_timestamp.timestamp(),
        "end_timestamp": end_timestamp.timestamp(),
        "api_service": API_SERVICE,
        "auth_id": AUTH_ID,
        "auth_secret": AUTH_SECRET,
        "x_chain_id": X_CHAIN_ID,
    })

    ##########################################
    ### Export blocks and transactions
    ##########################################
    _export_enrich_block_group_command(
        start_timestamp=start_timestamp,
        start_block=start_block,
        end_block=end_block,
        provider_uri=PROVIDER_URI,
        max_workers = export_max_workers,
        batch_size = export_batch_size,
        file_format = "json",
        file_maxlines = None,
        compress = False,
        **{
            "api_service": API_SERVICE,
            "auth_id": AUTH_ID,
            "auth_secret": AUTH_SECRET,
            "x_chain_id": X_CHAIN_ID,
        })

    task_manager.task_finished(TaskIDs["ALL"], "raw", start_timestamp, end_timestamp)
