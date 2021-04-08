import uuid

from loguru import logger


class RequestID(object):
    def __init__(self, app, header_name="X-Request-ID"):
        self.app = app.wsgi_app
        self._header_name = header_name
        self._flask_header_name = header_name.upper().replace("-", "_")
        app.wsgi_app = self

    def __call__(self, environ, start_response):
        header_key = "HTTP_{0}".format(self._flask_header_name)
        if not environ.get(header_key):
            environ.setdefault(header_key, str(uuid.uuid4()))
        req_id = environ[header_key]
        environ["FLASK_REQUEST_ID"] = req_id

        def new_start_response(status, response_headers, exc_info=None):
            response_headers.append((self._header_name, req_id))
            return start_response(status, response_headers, exc_info)

        with logger.contextualize(ID=req_id):
            return self.app(environ, new_start_response)