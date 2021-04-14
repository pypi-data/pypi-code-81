import pandas as pd
import json
from covid_cloud_client import COVIDCloud
# Creating the search client
search_url = 'https://ga4gh-search-adapter-presto-covid19-public.prod.dnastack.com/'
covid_client = COVIDCloud(search_url=search_url)


# Downloading meta-data
print('Fetching metadata from COVID Cloud…')
query = 'SELECT * FROM coronavirus_dnastack_curated.covid_cloud_production.sequences_view'
meta_data = json.loads(covid_client.query(query))
meta_df = pd.DataFrame(meta_data)
print("Metaata:")
print(meta_df)

# downloading variant-data
print('Fetching variants from COVID Cloud…')
query = 'SELECT * FROM coronavirus_dnastack_curated.covid_cloud_production.variants_flattened_view'
variant_data = json.loads(covid_client.query(query))
variant_df = pd.DataFame(covid_client.query(query))
print("Variant Data:")
print(variant_df)