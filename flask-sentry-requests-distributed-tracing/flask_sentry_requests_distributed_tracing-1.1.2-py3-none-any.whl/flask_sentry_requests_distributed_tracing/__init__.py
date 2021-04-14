from uuid import uuid4
from functools import wraps
import requests
from flask import request
import sentry_sdk


def flask_sentry_requests_distributed_tracing(app):
    with app.app_context():
        # NOTE: Setting here so it is present in crons/workers running in flask context
        sentry_sdk.set_tag("request-id", str(uuid4()))

        @app.before_request
        def _setup_sentry_scope():
            request_id = str(request.headers.get("x-request-id") or uuid4())
            sentry_sdk.set_tag("request-id", request_id)

    def _header_wrapper(f):
        @wraps(f)
        def wrapper(*args, **kwgs):
            with sentry_sdk.configure_scope() as scope:
                request_id = scope._tags.get("request-id") or str(uuid4())
                headers = kwgs.pop("headers", None) or {}
                headers["x-request-id"] = request_id
                return f(*args, headers=headers, **kwgs)

        return wrapper

    if getattr(requests, "__flask_sentry_requests_distributed_tracing_patch", False):
        return
    setattr(requests, "__flask_sentry_requests_distributed_tracing_patch", True)

    requests.Session.request = _header_wrapper(requests.Session.request)
