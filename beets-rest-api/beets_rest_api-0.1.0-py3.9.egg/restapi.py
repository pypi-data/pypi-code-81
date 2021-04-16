import base64
import json
import os

import flask
from beets import ui, library, util
from beets.plugins import BeetsPlugin
from flask import g, request

app = flask.Flask(__name__)


def _to_json(obj):
    out = dict(obj)

    if isinstance(obj, library.Item):
        if app.config.get('INCLUDE_PATHS', False):
            out['path'] = util.displayable_path(out['path'])
        else:
            del out['path']

        for key, value in out.items():
            if isinstance(out[key], bytes):
                out[key] = base64.b64encode(value).decode('ascii')

        try:
            out['size'] = os.path.getsize(util.syspath(obj.path))
        except OSError:
            out['size'] = 0

        return out

    elif isinstance(obj, library.Album):
        if app.config.get('INCLUDE_PATHS', False):
            out['artpath'] = util.displayable_path(out['artpath'])
        else:
            del out['artpath']
        return out


def _json_list(items):
    yield '['
    first = True
    for item in items:
        if first:
            first = False
        else:
            yield ','
        yield json.dumps(_to_json(item))
    yield ']'


@app.before_request
def before_request():
    g.lib = app.config['lib']


@app.route('/items', methods=["GET"])
def item_query():
    query = request.args.get('query')
    result = g.lib.items(query)
    return app.response_class(_json_list(result), mimetype='application/json')


@app.route('/item/<int:item_id>/file')
def item_file(item_id):
    item = g.lib.get_item(item_id)

    if not item:
        return flask.abort(404)

    item_path = util.py3_path(item.path)

    try:
        unicode_item_path = util.text_string(item.path)
    except (UnicodeDecodeError, UnicodeEncodeError):
        unicode_item_path = util.displayable_path(item.path)

    base_filename = os.path.basename(unicode_item_path)

    response = flask.send_file(
        item_path,
        as_attachment=True,
        attachment_filename=base_filename
    )
    response.headers['Content-Length'] = os.path.getsize(item_path)
    return response


@app.route('/album/<int:album_id>/art')
def album_art(album_id):
    album = g.lib.get_album(album_id)

    if not item:
        return flask.abort(404)

    item_path = util.py3_path(item.path)

    try:
        unicode_item_path = util.text_string(item.path)
    except (UnicodeDecodeError, UnicodeEncodeError):
        unicode_item_path = util.displayable_path(item.path)

    base_filename = os.path.basename(unicode_item_path)

    response = flask.send_file(
        item_path,
        as_attachment=True,
        attachment_filename=base_filename
    )
    response.headers['Content-Length'] = os.path.getsize(item_path)
    return response

class RestApiPlugin(BeetsPlugin):

    def __init__(self):
        super(RestApiPlugin, self).__init__()

        self.config.add({
            'host': u'127.0.0.1',
            'port': 8338
        })

    def commands(self):
        cmd = ui.Subcommand('restapi', help=u'start a REST api server')

        def func(lib, opts, args):
            args = ui.decargs(args)

            if args:
                self.config['host'] = args.pop(0)
            if args:
                self.config['port'] = int(args.pop(0))

            app.config['lib'] = lib
            app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
            app.config['log'] = self._log

            app.run(host=self.config['host'].as_str(),
                    port=self.config['port'].get(int))

        cmd.func = func
        return [cmd]
