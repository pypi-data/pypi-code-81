# -*- coding: utf-8 -*-
'''
Spiro CI receiving server.

Takes the following configuration arguments:
* port: Port to listen on, defaults to 4510
* ssl_key: The private key for TLS
* ssl_crt: The public certificate for TLS

If ssl_key/ssl_crt are not given, plain HTTP without TLS is used. If one is
given, that is an error.

Creates an HTTP server at the given port. It has one path, /, which accepts two
methods:

* GET: Checks the given token is valid, returning either a 401 Unauthorized or
  200 OK
* POST: Submits a deployment. Take form-like data (multipart/form-data):
  * project: The name of the project
  * deployment: The name of the deployment for the given project
  * highstate: If given, highstates affected minions (ie those with topfile
    entries for the given deployment)
  * bundle: Uploaded file: an uncompressed tar containing the files that make up
    the new deployment

The POST returns a text/event-stream, with the caveat that it is not resumable.
If the connection is left open, deployment updates are sent to the client where
the event is a code representing the stage and the data is a JSON. All messages
include a msg property, which is the human-readable status.

Deployment stages are:
* deploy-bundle: The uploaded bundle is being extracted and any generation that
  happens is being done, args: msg
* highstate-calc: Calculating minions to highstate, args: msg
* highstate-start: We're begining to highstate minions, args: msg, minions
* highstate-update: A minion has finished its highstate, args: msg, minion,
  result (big blob of highstate data)
* highstate-finish: The highstate has completed, args: msg

If there's an error, an exception message is sent with the args msg.

Authentication is HTTP Bearer auth, eg the client should be configured with a
token and send a header in the form of "Authorization: Bearer <token>". If no
token is given or is invalid (authentication fails), a 401 Unauthorized is
returned. If authorization fails (the given token is not allowed to deploy to
the given project), a 403 Forbidden is returned.
'''
from __future__ import absolute_import, print_function, unicode_literals
import tarfile
import logging
from salt.ext.tornado import ioloop
from salt.ext.tornado import iostream
from salt.ext.tornado import web
from salt.ext.tornado import gen
from salt.ext.tornado import queues
from salt.ext.tornado import httpserver
import json
import ssl
import os
import traceback
from salt.ext import six
from salt.client import LocalClient
from salt.runner import RunnerClient
from multiprocessing.pool import ThreadPool


log = logging.getLogger(__name__)


def log_exception(callback, *pargs, **kwargs):
    _error_func = None
    if '_error_func' in kwargs:
        _error_func = kwargs['_error_func']
        del kwargs['_error_func']
    try:
        callback(*pargs, **kwargs)
    except Exception as e:
        log.exception("Problem deploying")
        if _error_func is not None:
            try:
                _error_func(e)
            except Exception:
                log.exception("Problem running error handler")
        raise


def deploy_background(sendmsg, tarball, project, deployment, highstate=True):
    dep = __utils__['spiro.from_pd'](project, deployment)

    sendmsg("deploy-bundle", {"msg": "Deploying bundle"})
    dep.deploy_new(tarball)

    # TODO: Do we need to flush the fileserver?

    log.debug("Highstate: %r", highstate)
    if highstate:
        runner = RunnerClient(__opts__)
        minion = LocalClient(mopts=__opts__)
        sendmsg("highstate-calc", {"msg": "Calculating minions to highstate"})
        mids = runner.cmd('spiro.query_highstate', [dep.saltenv])
        if not mids:
            sendmsg("highstate-start", {
                "msg": "No minions to highstate",
                "minions": [],
            })
            sendmsg("highstate-finish", {
                "msg": "Highstate complete",
            })
        else:
            sendmsg("highstate-start", {
                "msg": "Highstating %i minions: %s" % (len(mids), ', '.join(mids)),
                "minions": mids,
            })
            for res in minion.cmd_iter(mids, 'state.highstate', tgt_type='list', kwarg={'queue': True, 'saltenv': dep.saltenv}, expect_minions=True):
                for mid, result in res.items():
                    sendmsg("highstate-update", {
                        "msg": "Minion %s finished" % mid,
                        "minion": mid,
                        "result": result,
                    })
            sendmsg("highstate-finish", {
                "msg": "Highstate complete",
            })
    sendmsg(None, None)


class SpiroBuildHandler(web.RequestHandler):
    pool = ThreadPool(10)

    def prepare(self):
        super(SpiroBuildHandler, self).prepare()
        log.info("Receved Headers: %r", self.request.headers)

        token = self.get_current_user()
        if not token or not __utils__['spiro_auth.check_token'](token):
            self.set_header('WWW-Authenticate', 'Bearer')
            self.send_error(401)

    def get_current_user(self):
        try:
            auth = self.request.headers['Authorization']
        except (KeyError, TypeError):
            return
        else:
            try:
                typ, token = auth.split(' ', 1)
            except Exception:
                return
            else:
                if typ.strip().lower() != 'bearer':
                    return
                return token.strip()

    def get(self):
        self.set_header("Content-Type", "text/plain")
        self.write("Auth OK")

    @gen.coroutine
    def sse_start(self):
        """Sets up SSE for later pushing"""
        try:
            self.set_header('Content-Type', 'text/event-stream')
            self.set_header('Cache-Control', 'no-cache')
            yield self.flush()
        except iostream.StreamClosedError:
            pass

    @gen.coroutine
    def sse_push(self, data, event=None):
        """Pushes data to a listener."""
        try:
            if event is not None:
                self.write('event: %s\n' % event)
            self.write('data: %s\n\n' % json.dumps(data))
            yield self.flush()
        except iostream.StreamClosedError:
            pass

    def _check_path(self, pathname):
        # TODO: Check that this pathname is safe to extract
        return True

    @gen.coroutine
    def post(self):
        # 1. Check parameters, open tarball
        # 2. Write out files
        # 3. (Optional) Highstate touched minions
        log.debug("Received deploy")
        project = self.get_argument('project')
        deployment = self.get_argument('deployment')
        highstate = bool(self.get_argument('highstate', default=''))
        files = self.request.files['bundle']

        if not __utils__['spiro_auth.check_token'](self.get_current_user(), project):
            self.send_error(403)

        if len(files) != 1:
            self.send_error(400)  # TODO: Be more specific
        try:
            tarball = tarfile.open(fileobj=six.BytesIO(files[0].body))
            # Check validity of tarball
            bundle = tarball.getmembers()
        except tarfile.TarError:
            self.send_error(400)  # TODO: Be more specific

        if not all(self._check_path(ti.name) for ti in bundle):
            self.send_error(400)  # TODO: Be more specific

        log.debug("Starting deploy")
        # At this point, we have accepted the submission and start work
        yield self.sse_start()

        queue, sendmsg = self.mkqueue()

        def _error(exc):
            sendmsg(
                'exception',
                {'msg': ''.join(traceback.format_exception_only(type(exc), exc))}
            )
            sendmsg(None, None)

        res = self.pool.apply_async(
            log_exception,
            (deploy_background, sendmsg, tarball, project, deployment, highstate),
            {'_error_func': _error},
            # error_callback=_error,  # Py3 only
        )

        while True:
            event, data = yield queue.get()
            if event is None:
                break
            else:
                yield self.sse_push(data, event)

    def mkqueue(self):
        loop = ioloop.IOLoop.current()
        q = queues.Queue()

        def sendmsg(event, data):
            loop.add_callback(
                q.put, (event, data)
            )
        return q, sendmsg


def make_app():
    return web.Application([
        (r"/", SpiroBuildHandler),
    ])


def make_server(app, cert, key):
    if (cert and not os.path.exists(cert)) or (key and not os.path.exists(key)):
        log.error("SSL cert/key do not exist, starting without")
        cert = key = None
    if not cert:
        log.info("Clearnet server")
        return httpserver.HTTPServer(app)
    else:
        log.info("Encrypted server")
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(cert, key)

        # Protocol options: allow TLSv1.1 and later
        ssl_ctx.options |= ssl.OP_NO_SSLv2
        ssl_ctx.options |= ssl.OP_NO_SSLv3
        ssl_ctx.options |= ssl.OP_NO_TLSv1
        ssl_ctx.options |= ssl.OP_NO_TLSv1_1

        # Cipher options: strong ciphers, follow server preferences
        # From https://wiki.mozilla.org/Security/Server_Side_TLS#Modern_compatibility
        ssl_ctx.set_ciphers("ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256")
        ssl_ctx.options |= ssl.OP_CIPHER_SERVER_PREFERENCE

        # Key exchange: strong prime curve, no point reuse
        ssl_ctx.set_ecdh_curve('prime256v1')
        ssl_ctx.options |= ssl.OP_SINGLE_ECDH_USE

        return httpserver.HTTPServer(app, ssl_options=ssl_ctx, max_buffer_size=10*1024*1024*1024)


def start(port=4510, ssl_crt=None, ssl_key=None):
    '''
    Start the server for spiro to receive uploads from CI
    '''
    with open('/tmp/opts', 'wt') as f:
        import pprint
        pprint.pprint(__opts__, stream=f)
    log.info("Engine start: port=%r, ssl_crt=%r, ssl_key=%r", port, ssl_crt, ssl_key)
    if __opts__['__role'] == 'master':
        app = make_app()
        server = make_server(app, ssl_crt, ssl_key)
        server.listen(port)
        log.info("Starting SpiroFS Deployment Server on port %s", port)
        ioloop.IOLoop.current().start()
    else:
        # Don't do anything as the minion
        # TODO: Can we say "No, don't restart us?"
        pass
