'''
Spiro fileserver backend
'''
from __future__ import absolute_import, print_function, unicode_literals
import logging

import salt.utils.gzip_util
import salt.utils.files
from salt.ext import six

log = logging.getLogger(__name__)

log.info("load")

__virtualname__ = 'spiro'


def __virtualname__():
    if __virtualname__ not in __opts__['fileserver_backend']:
        return False
    return __virtualname__


def envs():
    log.info("envs")
    return [d.saltenv for d in __utils__['spiro.list_deployments']()]


def update():
    log.info("update")


def file_list(load):
    log.info("file_list: %r", load)
    deployment = __utils__['spiro.from_env'](load['saltenv'])
    if deployment is None:
        return []
    else:
        return [
            fn
            for fn, t in deployment.contents()
            if t == 'f'
        ]


def file_list_emptydirs(load):
    log.info("file_list_emptydirs: %r", load)
    deployment = __utils__['spiro.from_env'](load['saltenv'])
    if deployment is None:
        return []
    else:
        return [
            fn
            for fn, t in deployment.contents()
            if t == 'e'
        ]


def dir_list(load):
    log.info("dir_list: %r", load)
    deployment = __utils__['spiro.from_env'](load['saltenv'])
    if deployment is None:
        return []
    else:
        return [
            fn
            for fn, t in deployment.contents()
            if t == 'd'
        ]


def symlink_list(load):
    log.info("symlink_list: %r", load)
    return {}
    # FIXME: Make mapping of link -> dest
    deployment = __utils__['spiro.from_env'](load['saltenv'])
    if deployment is None:
        return []
    else:
        return [
            fn
            for fn, t in deployment.contents()
            if t == 's'
        ]


def find_file(path, saltenv='base', **kwargs):
    log.info("find_file: %r, %r, **%r", path, saltenv, kwargs)
    dep = __utils__['spiro.from_env'](saltenv)
    if dep is None:
        return {}
    else:
        return {
            'path': path,
            'deployment': dep.serialize() if dep.exists(path) else None,
        }


def file_hash(load, fnd):
    log.info("file_hash: %r, %r", load, fnd)
    dep = __utils__['spiro.deserialize'](fnd.get('deployment'))
    if dep is None:
        return {}

    return {
        'hsum': dep.hash_file(fnd['path'], __opts__['hash_type']),
        'hash_type': __opts__['hash_type'],
    }


def serve_file(load, fnd):
    # fnd is the return of find_file()
    log.info("serve_file: %r, %r", load, fnd)
    dep = __utils__['spiro.deserialize'](fnd.get('deployment'))
    if dep is None:
        return {'data': '', 'dest': ''}

    gzip = load.get('gzip')

    with dep.open(fnd['path'], 'rb') as f:
        f.seek(load['loc'])

        data = f.read(__opts__['file_buffer_size'])
        # TBH, I'm not sure why this exists, and it causes problems
        # if data and six.PY3 and not salt.utils.files.is_binary(fnd['path']):
        #     data = data.decode(__salt_system_encoding__)
        if gzip and data:
            data = salt.utils.gzip_util.compress(data, gzip)
            return {
                'data': data,
                'dest': fnd['path'],
                'gzip': gzip,
            }
        else:
            return {
                'data': data,
                'dest': fnd['path'],
            }
