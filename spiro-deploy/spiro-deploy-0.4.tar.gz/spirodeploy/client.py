"""
Handling the actual upload
"""
import json
import requests
import socket
import urllib3

__all__ = ('upload',)


class HTTPAdapterWithKeepalive(requests.adapters.HTTPAdapter):
    # Keepalive parameters
    interval_sec = 30
    idle_sec = interval_sec
    max_fails = 5
    def init_poolmanager(self, *args, **kwargs):
        sockopts = urllib3.connection.HTTPConnection.default_socket_options + []
        if hasattr(socket, 'SO_KEEPALIVE'):
            # Not Windows
            sockopts += [
                (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
            ]
        if hasattr(socket, 'TCP_KEEPALIVE'):
            # Mac
            sockopts += [
                (socket.IPPROTO_TCP, socket.TCP_KEEPALIVE, self.interval_sec)
            ]
        if hasattr(socket, 'TCP_KEEPIDLE'):
            # Linux
            sockopts += [
                (socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, self.idle_sec)
            ]
        if hasattr(socket, 'TCP_KEEPINTVL'):
            # Linux
            sockopts += [
                (socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, self.interval_sec)
            ]
        if hasattr(socket, 'TCP_KEEPCNT'):
            # Linux
            sockopts += [
                (socket.IPPROTO_TCP, socket.TCP_KEEPCNT, self.max_fails)
            ]
        # Windows:
        # sock.ioctl(socket.SIO_KEEPALIVE_VALS, (<1 to turn on>, <idle time in ms>, <interval in ms>))
        # https://msdn.microsoft.com/en-us/library/dd877220%28v=vs.85%29.aspx
        super().init_poolmanager(*args, socket_options=sockopts, **kwargs)


def get_session():
    adapter = HTTPAdapterWithKeepalive()
    s = requests.session()
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s


def stream_raw_sse(mkrequest, *pargs, _last_event_id=None, headers=None, **kwargs):
    """
    Streams Server-Sent Events, each event produced as a sequence of
    (field, value) pairs.

    Does not handle reconnection, etc.
    """
    if headers is None:
        headers = {}
    headers['Accept'] = 'text/event-stream'
    headers['Cache-Control'] = 'no-cache'
    # Per https://html.spec.whatwg.org/multipage/server-sent-events.html#sse-processing-model
    if _last_event_id is not None:
        headers['Last-Event-ID'] = _last_event_id

    with mkrequest(*pargs, headers=headers, stream=True, **kwargs) as resp:
        resp.raise_for_status()
        fields = []
        for line in resp.iter_lines(decode_unicode=True):
            # https://html.spec.whatwg.org/multipage/server-sent-events.html#event-stream-interpretation
            if not line:
                yield fields
                fields = []
            elif line.startswith(':'):
                pass
            elif ':' in line:
                field, value = line.split(':', 1)
                if value.startswith(' '):
                    value = value[1:]
                fields += [(field, value)]
            else:  # Non-blank, without a colon
                fields += [(line, '')]


def less_raw(msgs):
    """
    Wrap around stream_raw_sse() to get spiro-deploy data.
    """
    for msg in msgs:
        msg = dict(msg)
        yield msg.get('event'), json.loads(msg.get('data'))


def upload(url, token, tarball, project, deployment, highstate=True, sslverify=True, connect_timeout=20):
    """
    Do the upload&deploy thing
    """
    fields = {
        'project': project,
        'deployment': deployment,
    }
    if highstate:
        fields['highstate'] = True
    tarball.seek(0)
    files = {
        'bundle': tarball,
    }
    http = get_session()
    for event, data in less_raw(stream_raw_sse(
        http.post,
        url,
        data=fields,
        files=files,
        headers={'Authorization': 'bearer {}'.format(token)},
        verify=sslverify,
        timeout=(None, None),
    )):
        yield event, data
