import pandas as pd

def create_xlsx(systems, path, primary_column_name='full_name'):
	df = pd.DataFrame(systems)
	df.set_index(primary_column_name, inplace=True)
	df.to_excel(path)
	return
