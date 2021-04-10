class DeprecatedLibrary(Exception):
	def __init__(self, library, funName, line):
		self.library = library
		self.funName = funName
		self.line = line
		self.message = f"Il sito è cambiato, di conseguenza la libreria {library} è DEPRECATA. -> [{library}.{funName} - {line}]"
		super().__init__(self.message)