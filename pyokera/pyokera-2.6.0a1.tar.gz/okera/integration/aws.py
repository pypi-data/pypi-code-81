import logging

from okera.integration import boto as okera_boto

LOG = logging.getLogger(__name__)

_VALID_COMMANDS = ['s3', 's3api']
_CONFIG_KEY_OKERA = 'okera'
_CONFIG_KEY_REST = 'rest'
_CONFIG_KEY_PROXY = 'proxy'
_CONFIG_KEY_TOKEN = 'token'

def _get_info_from_profile(profile):
    proxy_endpoint = None
    rest_endpoint = None
    token = None

    if _CONFIG_KEY_OKERA not in profile:
        return None

    info = profile[_CONFIG_KEY_OKERA]
    if _CONFIG_KEY_PROXY not in info \
        or _CONFIG_KEY_REST not in info \
        or _CONFIG_KEY_TOKEN not in info:
        return None

    proxy_endpoint = profile[_CONFIG_KEY_OKERA][_CONFIG_KEY_PROXY]
    rest_endpoint = profile[_CONFIG_KEY_OKERA][_CONFIG_KEY_REST]
    token = profile[_CONFIG_KEY_OKERA][_CONFIG_KEY_TOKEN]

    return proxy_endpoint, rest_endpoint, token

def _register_okera_proxy(parsed_args, **kwargs):
    if parsed_args.debug:
        LOG.setLevel(logging.DEBUG)

    if not parsed_args.command:
        LOG.debug("No command")
        return

    command = parsed_args.command.lower()
    if command not in _VALID_COMMANDS:
        LOG.debug("Not valid command: %s" % command)
        return

    if 'session' not in kwargs or not kwargs['session']:
        LOG.debug("No session")
        return

    session = kwargs['session']
    if parsed_args.profile:
        session.set_config_variable('profile', parsed_args.profile)

    okera_info = _get_info_from_profile(session.get_scoped_config())
    if not okera_info:
        LOG.debug("No Okera configuration found")
        return

    LOG.debug("Injecting Okera proxy")
    proxy, rest, token = okera_info

    okera_session = okera_boto.okera_session(session, token, rest, proxy)
    kwargs['session'] = okera_session

    # TODO: rather than setting this, we should automatically
    # retrieve the CA bundle from the server and set it so we
    # still validate it.
    parsed_args.verify_ssl = False

def awscli_initialize(cli):
    cli.register('top-level-args-parsed', _register_okera_proxy)