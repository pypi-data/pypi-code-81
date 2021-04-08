# -*- coding: utf-8 -*-
import os
import logging
import json
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from onelogin.saml2.idp_metadata_parser import OneLogin_Saml2_IdPMetadataParser
from pyramid.httpexceptions import HTTPFound, HTTPOk, HTTPInternalServerError


__VERSION__ = '0.0.1'


log = logging.getLogger('pyramid_saml')
"""logging.Logger: Logger instance for log output."""


SAML_NAME_ID = 'samlNameId'
"""str: Key of the NameId attribute."""

SAML_USER_DATA = 'samlUserData'
"""str: Key of the UserData attribute."""

SAML_SESSION_INDEX = 'samlSessionIndex'
"""str: Key of the SessionIndex attribute."""

SAML_ERROR = 'samlError'
"""str: Key of the Error attribute."""


class SAML(object):
    def __init__(self, request):
        """The SAML object, providing the view methods.

        Args:
            request (pyramid.request.Request): The Pyramid request object.
        """

        self._request = request
        """pyramid.request.Request: The current request object."""

        self._session = self._request.session
        """dict: The current request's session instance."""

        self._settings = self._request.registry.settings.get('pyramid_saml')
        """dict: The parsed `pyramid_saml` settings."""

        # Lowercase URL encoding is needed for ADFS
        lowercase = self._settings.get('lowercase_urlencoding') or False

        saml_path = self._settings.get('saml_path')
        self._saml_path = os.path.dirname(__file__) \
            if saml_path is None \
            else saml_path
        """str: Directory containing the settings.json and certificates."""

        # Name of a default route as fallback for redirects
        self._index_url = self._request.route_url(
            self._settings.get('index_route_name')
        )
        """str: Index route URL."""

        self._saml_request = {
            'https': 'on' if request.scheme == 'https' else 'off',
            'http_host': request.host,
            'server_port': request.server_port,
            'script_name': request.path,
            'get_data': request.GET.copy(),
            'lowercase_urlencoding': lowercase,
            'post_data': request.POST.copy(),
        }
        """dict: The SAML request configuration."""

        self.auth = OneLogin_Saml2_Auth(
            self._saml_request,
            self._settings,
            custom_base_path=self._saml_path
        )
        """onelogin.saml2.auth.OneLogin_Saml2_Auth: The current auth
                object.
        """

    def sso(self):
        """Performs the login request.

        Returns:
            pyramid.httpexceptions.HTTPFound: Redirect to the IdP.
        """
        if 'redirect' in self._request.params:
            return_to = self._request.params.get('redirect')
        else:
            return_to = self._index_url
        return HTTPFound(self.auth.login(return_to))

    def slo(self):
        """Performs the logout request.

        Returns:
            pyramid.httpexceptions.HTTPFound: Redirect to the IdP.
        """
        name_id = None
        session_index = None
        if SAML_NAME_ID in self._session:
            name_id = self._session[SAML_NAME_ID]
        if SAML_SESSION_INDEX in self._session:
            session_index = self._session[SAML_SESSION_INDEX]
        return HTTPFound(self.auth.logout(
            name_id=name_id,
            session_index=session_index
        ))

    def acs(self):
        """Process the IdP's login response.

        Returns:
            pyramid.httpexceptions.HTTPFound: Redirect to specified URL or
                configured index.
        """
        self.auth.process_response()
        errors = self.auth.get_errors()
        if len(errors) == 0:
            self._session[SAML_USER_DATA] = self.auth.get_attributes()
            self._session[SAML_NAME_ID] = self.auth.get_nameid()
            self._session[SAML_SESSION_INDEX] = self.auth.get_session_index()
            self._session[SAML_ERROR] = None
            self_url = OneLogin_Saml2_Utils.get_self_url(self._saml_request)
            if 'RelayState' in self._request.POST \
                    and self_url != self._request.POST['RelayState']:
                url = self.auth.redirect_to(self._request.POST['RelayState'])
                return HTTPFound(url)
        else:
            msg = self.auth.get_last_error_reason()
            log.error(msg)
            self._session[SAML_ERROR] = msg
        return HTTPFound(self._index_url)

    def sls(self):
        """Process the IdP's logout response.

        Returns:
            pyramid.httpexceptions.HTTPFound: Redirect to specified URL or
                configured index.
        """

        def delete_session_cb():
            """Callback function to clear the current session."""
            self._session.clear()

        url = self.auth.process_slo(delete_session_cb=delete_session_cb)
        errors = self.auth.get_errors()
        if len(errors) > 0:
            log.error(self.auth.get_last_error_reason())
            self._session[SAML_ERROR] = self.auth.get_last_error_reason()
        if url is not None:
            return HTTPFound(url)
        else:
            return HTTPFound(self._index_url)

    def metadata(self):
        """Returns the SP's metadata.

        Returns:
            pyramid.httpexceptions.HTTPOk: The rendered metadata.

        Raises:
            pyramid.httpexceptions.HTTPInternalServerError: The metadata
                error.
        """
        settings = self.auth.get_settings()
        metadata = settings.get_sp_metadata()
        errors = settings.validate_metadata(metadata)

        if len(errors) > 0:
            raise HTTPInternalServerError(', '.join(errors))

        return HTTPOk(body=metadata, headers={'Content-Type': 'text/xml'})


def _load_settings_from_file(config):
    """Parse configuration from `settings.json` and `advanced_settings.json`.

    Args:
        config (pyramid.config.Configurator): The configuration of the
            existing Pyramid application.
    """

    saml_path = config.get_settings().get('pyramid_saml').get('saml_path')

    with open(os.path.join(saml_path, 'settings.json')) as f:
        config.get_settings().get('pyramid_saml').update(
            json.loads(f.read())
        )

    if os.path.isfile(os.path.join(saml_path, 'advanced_settings.json')):
        with open(os.path.join(saml_path, 'advanced_settings.json')) as f:
            config.get_settings().get('pyramid_saml').update(
                json.loads(f.read())
            )


def _load_settings_from_url(config):
    """Parse configuration from IdP metadata.

    Args:
        config (pyramid.config.Configurator): The configuration of the
            existing Pyramid application.
    """

    settings = config.get_settings().get('pyramid_saml')

    metadata_url = entity_id = None
    if 'metadata_url' in settings:
        metadata_url = settings.get('metadata_url')
    if 'PYRAMID_SAML_METADATA_URL' in os.environ:
        metadata_url = os.environ.get('PYRAMID_SAML_METADATA_URL')
    if 'idp' in settings and 'entityId' in settings.get('idp'):
        entity_id = settings.get('idp').get('entityId')
    if 'PYRAMID_SAML_IDP_ENTITY_ID' in os.environ:
        entity_id = os.environ.get('PYRAMID_SAML_IDP_ENTITY_ID')

    if metadata_url is not None:
        metadata = OneLogin_Saml2_IdPMetadataParser.parse_remote(
            metadata_url,
            entity_id=entity_id
        )
        log.debug('Parsed IDP metadata:\n{0}'.format(
            json.dumps(metadata, indent=4)
        ))
        if 'idp' in settings:
            config.get_settings()['pyramid_saml']['idp'].update(
                metadata['idp']
            )
        else:
            config.get_settings()['pyramid_saml']['idp'] = metadata['idp']


def _load_settings(config):
    """Parse and validate SAML configuration.

    Args:
        config (pyramid.config.Configurator): The configuration of the
            existing Pyramid application.
    """

    if 'PYRAMID_SAML_PATH' in os.environ:
        if 'pyramid_saml' not in config.get_settings():
            config.get_settings().update({
                'pyramid_saml': {}
            })
        config.get_settings().get('pyramid_saml').update({
            'saml_path': os.environ.get('PYRAMID_SAML_PATH')
        })

    if 'pyramid_saml' not in config.get_settings():
        msg = 'Missing \'pyramid_saml\' configuration in settings'
        raise AssertionError(msg)
    else:
        settings = config.get_settings().get('pyramid_saml')

    if 'saml_path' not in settings:
        msg = 'Missing \'saml_path\' in settings'
        raise AssertionError(msg)
    else:
        saml_path = settings.get('saml_path')
        log.debug('SAML path: {0}'.format(saml_path))

    _load_settings_from_file(config)
    _load_settings_from_url(config)

    log.debug('SAML config:\n{0}'.format(json.dumps(
        config.get_settings().get('pyramid_saml'),
        indent=4
    )))


def includeme(config):  # pragma: no cover
    """Include this library in an existing Pyramid application.

    Args:
        config (pyramid.config.Configurator): The configuration of the
            existing Pyramid application.
    """

    # Set log level through env variable
    log_level = '{0}'.format(os.environ.get('PYRAMID_SAML_LOG_LEVEL')).lower()
    if log_level == 'error':
        log.setLevel(logging.ERROR)
    elif log_level == 'warning':
        log.setLevel(logging.WARNING)
    elif log_level == 'debug':
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    config.add_route('pyramid_saml_sso', '/sso')
    config.add_view(
        SAML,
        attr='sso',
        route_name='pyramid_saml_sso'
    )

    config.add_route('pyramid_saml_slo', '/slo')
    config.add_view(
        SAML,
        attr='slo',
        route_name='pyramid_saml_slo'
    )

    config.add_route('pyramid_saml_acs', '/acs')
    config.add_view(
        SAML,
        attr='acs',
        route_name='pyramid_saml_acs'
    )

    config.add_route('pyramid_saml_sls', '/sls')
    config.add_view(
        SAML,
        attr='sls',
        route_name='pyramid_saml_sls'
    )

    config.add_route('pyramid_saml_metadata', '/metadata')
    config.add_view(
        SAML,
        attr='metadata',
        route_name='pyramid_saml_metadata'
    )

    # Load SAML settings and append them to the application settings
    _load_settings(config)
