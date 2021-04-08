'''
Runners for handling spiro-managed saltenvs
'''
from __future__ import absolute_import, print_function, unicode_literals
import logging
from salt.ext import six


log = logging.getLogger(__name__)


def query_highstate(saltenv):
    """
    Return the list of minions that have tops in the given saltenv.

    If the given saltenv has changed, these minions might be effected.

    Note that this is generally useful and does not require the use of spirofs.

    Note: This assumes you do not have any Jinja in your top files that mutates your systems.
    """
    tops = __salt__['salt.execute']('*', 'state.show_top', kwarg={'concurrent': True})
    return [
        mid
        for mid, envs in tops.items()
        if envs and saltenv in envs
    ]


def issue_token(projects, lifespan=None):
    """
    Issue a deployment token for the given projects, optionally for the given time (in seconds)
    """
    if isinstance(projects, six.string_types):
        projects = projects.split(',')

    if lifespan is not None:
        lifespan = int(lifespan)

    return __utils__['spiro_auth.generate_token'](projects=projects, lifespan=lifespan)


def issue_root_token(lifespan=None):
    """
    Issue a deployment token for all projects, optionally for the given time (in seconds)
    """
    if lifespan is not None:
        lifespan = int(lifespan)

    return __utils__['spiro_auth.generate_token'](lifespan=lifespan)


def revoke_token(token):
    """
    Revokes the given token, making it invalid and disallowing it from accessing
    anything.
    """
    log.warning("TODO: Implement revoke_token")


def check_token(token, project=None):
    """
    Checks if the given token is valid for the given project. If not project is
    given, only check that the token is valid.
    """
    return __utils__['spiro_auth.check_token'](token, project)


def inspect_token(token):
    """
    Gets the information embedded in the given token in a human-readable format.
    """
    return __utils__['spiro_auth.inspect_token'](token)

