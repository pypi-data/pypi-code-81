from pprint import pformat
from werkzeug.exceptions import HTTPException
from flask import (
    jsonify,
    session,
    request,
    has_request_context,
)
from ._base import BaseApiError, JsonResponse


class FlaskApiError(BaseApiError, HTTPException):
    errno = 40000
    code = 400
    msg = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.code = self.status
        self.description = JsonResponse.describe_status(self.status)

    def _gen_printable_item(self):
        if has_request_context():
            uid = session.get('user_id', '')
            u = session.get('username', '')
            yield f'{request.method} {request.full_path} {self.status} - {uid}:{u}:{self.request_id}'
            yield f'[{request.endpoint}] {request.view_args}'
            # yield f'[$Form] {pformat(request.form_json)}'
        yield self.description
        if self.kwargs:
            yield f'[kwargs] {pformat(self.kwargs, indent=2)}'

    def __str__(self):
        return "\n\t".join(map(str, self._gen_printable_item()))

    def get_response(self, environ=None):
        result = self.to_dict(environ=environ)
        return jsonify(result), self.status
