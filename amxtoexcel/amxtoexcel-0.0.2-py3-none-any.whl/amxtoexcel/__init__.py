import pandas as pd
from logging import info

def create_xlsx(systems, path, primary_column_name='full_name'):
	df = pd.DataFrame(systems)
	df.set_index(primary_column_name, inplace=True)
	df.to_excel(path)
	info(f"{__name__} created {path}")
	return
