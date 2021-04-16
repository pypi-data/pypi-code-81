"""
WSGI application builder.
"""
import sys
from . import logger
from .webapp import WebApp
from .settings import load_project
from .functions import Function, Project


def build_app(path: str):
	r = load_project(path)
	sys.path.insert(1, path)
	p = Project(r["project"])
	params = []
	for f in r["functions"]:
		try:
			t = Function(*f)
			url = "{}/{}".format(p.route_prefix, t.trigger.route)
			logger.info("[{}] {} {}".format(t.func_name, ", ".join(t.trigger.methods).upper(), url))
			params.append((
				url,
				t.trigger.methods,
				t.load_main(),
				t.trigger.name
			))
		except ValueError as e:
			logger.warning("[{}] Unable to mount Function: {}".format(f[0], e))
	return WebApp(params)
