"""
WebApp.
"""
import re
from urllib.parse import parse_qs
from typing import Tuple, List, Callable
import azure.functions as func
from . import logger


class HTTPError(Exception):
	pass


class NotFound(HTTPError):
	pass


class MethodNotAllowed(HTTPError):
	pass


class WebApp:

	NOT_FOUND = func.HttpResponse(status_code=404)
	METHOD_NOT_ALLOWED = func.HttpResponse(status_code=405)
	SERVER_ERROR = func.HttpResponse(status_code=500)

	MESSAGES = {
		200: "OK",
		201: "Created",
		204: "No Content",
		301: "Moved Permanently",
		302: "Found",
		304: "Not Modified",
		401: "Unauthorized",
		403: "Forbidden",
		404: "Not Found",
		405: "Method Not Allowed",
		500: "Internal Server Error",
		503: "Service Unavailable"
	}

	def __init__(self, init_params: List[Tuple[str, List[str], Callable, str]]):
		# (route, methods, function, param_name)
		self.init_params = init_params
		self.find_params_names_regex = re.compile(r"\{(\w*?)\}")
		self.rules = []
		self.build_regex()
		
	def build_regex(self):
		for tup in self.init_params:
			params_names = self.find_params_names_regex.findall(tup[0])
			route_match_regex = re.compile(self.find_params_names_regex.sub("([^/]*?)", tup[0]) + "$")
			self.rules.append((route_match_regex, params_names, tup))

	def select_handler(self, method: str, path: str):
		for rule in self.rules:
			result = rule[0].match(path)
			if result is not None:
				if method not in rule[2][1]:
					raise MethodNotAllowed()
				else:
					return rule[2], dict(zip(rule[1], result.groups()))
		raise NotFound()

	def __call__(self, environ, start_response):
		return self.wsgi(environ, start_response)

	def environ_to_request(self, environ: dict, route_params: dict) -> func.HttpRequest:
		# query parameters
		args = parse_qs(environ["QUERY_STRING"])
		query = {}
		for key, value in args.items():
			query[key] = ",".join(value)
		# headers
		headers = {}
		for key in environ:
			if key.startswith("HTTP_"):
				headers[key.replace("HTTP_", "").replace("_", "-").lower()] = environ[key]
		# content length
		try:
			request_body_size = int(environ.get('CONTENT_LENGTH', 0))
		except (ValueError):
			request_body_size = 0

		return func.HttpRequest(
			environ["REQUEST_METHOD"],
			environ["PATH_INFO"],
			headers=headers,
			route_params=route_params,
			params=query,
			body=environ['wsgi.input'].read(request_body_size)
		)

	def response_to_body(self, response: func.HttpResponse):
		return [response.get_body()]

	def get_status_message(self, status_code: int) -> str:
		try:
			return self.MESSAGES[status_code]
		except KeyError:
			return ""

	def process(self, environ: str) -> func.HttpResponse:
		try:
			handler, route_params = self.select_handler(
				environ["REQUEST_METHOD"].lower(),
				environ["PATH_INFO"]
			)
			request = self.environ_to_request(environ, route_params)
			return handler[2](**{handler[3]: request})
		except NotFound:
			return self.NOT_FOUND
		except MethodNotAllowed:
			return self.METHOD_NOT_ALLOWED
		except BaseException as e:
			logger.exception("")
			return self.SERVER_ERROR

	def wsgi(self, environ, start_response):
		response = self.process(environ)
		start_response(
			"{} {}".format(
				response.status_code,
				self.get_status_message(response.status_code)
			),
			response.headers.items()
		)
		return self.response_to_body(response)
