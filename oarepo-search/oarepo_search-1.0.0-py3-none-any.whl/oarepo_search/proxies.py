from flask import current_app
from werkzeug.local import LocalProxy

current_oarepo_search = LocalProxy(lambda: current_app.extensions['oarepo-search'])
