from airflow import DAG
from airflow.operators.python import PythonOperator
from jinja2 import Template
import dask.bag as db
from dask.distributed import Client
import json
from datetime import datetime
import logging
import dask

with DAG("neo_daily_ingestion",
         start_date=datetime(2021, 4, 1),
         schedule_interval='@daily',
         catchup=True) as dag:
    logger = logging.getLogger("airflow.task")
    dask.config.set(scheduler='threads')

    neo_url_template = Template(
        "https://api.nasa.gov/neo/rest/v1/feed?start_date={{start_date}}&end_date={{end_date}}&detailed=true&api_key=Xchr4nVfdtQacNDYRKtbd6R429oLF2BCsZUBIfrv")


    def denormalize(record, **kwargs):
        return [{'id': record['id'],
                 'name': record['name'],
                 'is_potentially_hazardous_asteroid': record['is_potentially_hazardous_asteroid'],
                 'close_approach_date': cad_record['close_approach_date'],
                 'miss_distance_miles': cad_record['miss_distance']['miles'],
                 'created_at': kwargs['processed_date']
                 }
                for cad_record in record['close_approach_data']]


    def ingest_neo_feed(**kwargs):
        client = Client(processes=False)
        created_at = kwargs['execution_date'].strftime('%Y-%m-%d')
        logger.info("created_at = " + created_at)
        neo_url = neo_url_template.render(start_date=created_at, end_date=created_at)
        logger.info("URL formed" + neo_url)
        neo_bag = db.read_text(neo_url)

        day_level = neo_bag.map(json.loads).pluck('near_earth_objects')
        day_level_bag = day_level.pluck(created_at)

        day_level_bag_denormalized = day_level_bag.flatten().map(denormalize, processed_date=created_at)
        neo_df = day_level_bag_denormalized.flatten().to_dataframe()
        logger.info(neo_df.head(5))
        neo_df.to_parquet(path='/tmp/data/neo_parquet', engine='fastparquet', partition_on=['created_at'])


    neo_ingest_task = PythonOperator(task_id=f"neo_ingest_task", python_callable=ingest_neo_feed, provide_context=True)
    neo_ingest_task
