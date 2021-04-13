import argparse

from http.server import HTTPServer

from core.settings import PORT
from core.request_handler import RequestHandler


def main():
	# Parse command line arguments.
	arg_parser = argparse.ArgumentParser(description='Open an HTML file.')
	arg_parser.add_argument('filename', metavar='filename', type=str, help='Name of the file')

	args = arg_parser.parse_args()
	with open('core/filename.py', 'w') as py_f:
		py_f.write(f"HTML_FILENAME = '{args.filename}'")

	# Host HTTP server.
	server = HTTPServer(('', PORT), RequestHandler)
	print(f'Server started on port {PORT}.')
	print(f'Can connect to: http:127.0.0.1:{PORT} or localhost:{PORT}.')
	server.serve_forever()


if __name__ == '__main__':
	main()
