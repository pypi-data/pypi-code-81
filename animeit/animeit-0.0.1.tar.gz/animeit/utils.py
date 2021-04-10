from .error import * # Importa le Exception globali

import inspect, os

def HealthCheck(fun): # Controlla se la libreria è deprecata
	def wrapper(*args, **kwargs):
		try:
			return fun(*args, **kwargs)
		except AttributeError:
			frame = inspect.trace()[-1]
			funName = frame[3]
			errLine = frame[2]
			library = frame[1].split(os.sep)[-2]
			raise DeprecatedLibrary(library, funName, errLine)
	return wrapper