"""Console script for grovec_sv_solution."""
import sys
import click
import duckdb
import dask.dataframe as ddf


@click.command()
def main():
    """Dask way of querying"""
    from dask.distributed import Client
    client = Client()
    neo_raw = ddf.read_parquet('/tmp/data/neo_parquet/*/*.parquet')
    neo_hazardous = neo_raw.loc[neo_raw['is_potentially_hazardous_asteroid']].compute()
    neo_hazardous_final = neo_hazardous[['id', 'name', 'close_approach_date', 'miss_distance_miles']]
    neo_hazardous_final.to_parquet(path='/tmp/data/neo_hazardous_result.parquet')

    # DuckDB way of querying
    cursor = duckdb.connect()
    cursor.execute("CREATE OR REPLACE VIEW neo_data AS SELECT * FROM parquet_scan('/tmp/data/neo_parquet/*/*.parquet')")
    print(cursor.execute(
        "SELECT id,name,miss_distance_miles FROM neo_data where is_potentially_hazardous_asteroid = True").fetchall())

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
