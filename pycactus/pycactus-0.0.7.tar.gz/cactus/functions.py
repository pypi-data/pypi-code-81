"""
Function entities.
"""
from importlib import import_module


class Project:
	def __init__(self, settings: dict):
		self.settings = settings

	@property
	def route_prefix(self):
		prefix = self.settings.get("extensions", {}).get("http", {}).get("routePrefix", "/")
		if not prefix.startswith("/"):
			prefix = "/" + prefix
		return prefix


class Binding:

	def __init__(self, settings: dict):
		self.settings = settings

	@property
	def type(self):
		return self.settings.get("type")

	@property
	def direction(self):
		return self.settings.get("direction")

	@property
	def name(self):
		return self.settings.get("name")


class HTTP(Binding):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.direction != "out":
			raise ValueError("http binding direction must be out")
		if self.name != "$return":
			raise ValueError("http binding name must be $return")


class HTTPTrigger(Binding):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.direction != "in":
			raise ValueError("httpTrigger binding direction must be in")
		if self.authLevel != "Anonymous":
			raise ValueError("httpTrigger binding authLevel must be Anonymous")

	@property
	def authLevel(self):
		return self.settings.get("authLevel", "Anonymous")

	@property
	def methods(self):
		return self.settings.get("methods", [])

	@property
	def route(self):
		return self.settings.get("route", [])


class Function:

	def __init__(self, func_name: str, settings: dict):
		self.settings = settings
		self.func_name = func_name
		temp = self.bindings
		if len(temp) > 2:
			raise ValueError("Maximum two bindings")
		a, b = tuple(temp)
		if b.type == "httpTrigger" and a.type == "http":
			t = a
			a = b
			b = t
		self.trigger = HTTPTrigger(a.settings)
		self.output = HTTP(b.settings)

	@property
	def bindings(self):
		return list(map(lambda x: Binding(x), self.settings.get("bindings", [])))
	
	@property
	def scriptFile(self):
		return self.settings.get("scriptFile")

	@property
	def script(self):
		return "{}.{}".format(self.func_name, self.scriptFile[:-3])
	
	def load_main(self):
		return getattr(import_module(self.script), "main")
