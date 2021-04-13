from http.server import BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
	"""Handles HTTP requests for the server."""
	
	def do_GET(self):
		"""Handle GET request."""
		self.send_response(200)
		self.send_header('content-type', 'text/html')
		self.end_headers()

		# Read html file content.
		from .filename import HTML_FILENAME
		with open(HTML_FILENAME, 'r') as html_f:
			html_content = html_f.read()

		self.wfile.write(html_content.encode())
