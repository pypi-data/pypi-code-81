import os, re

# Carica le librerie ######################################################################################

this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
base_path = os.path.join(this_dir, "libraries")


for job in os.listdir(base_path):

	# import_module(f"jobs.{myjob}")
	module = __import__(f"libraries.{job}", globals(),locals(), fromlist=["*"], level=1)

	for k in dir(module):
		locals()[k] = getattr(module, k)

# from error import * # Importa le Exception globali

############################################################################################################



# Funzione di 'cast'

def Anime(link):
	# lista pattern
	anime_world = re.compile(r"www\.animeworld\.tv")




	if anime_world.search(link) is not None:
		return AnimeWorld(link)