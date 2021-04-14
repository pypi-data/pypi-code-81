# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pluggy import HookspecMarker


hookspec = HookspecMarker("kadi")


@hookspec
def kadi_register_blueprints(app):
    """Hook for registering blueprints.

    For example (including a custom static path):

    .. code-block:: python3

        from flask import Blueprint

        bp = Blueprint(
            'my_plugin',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/my_plugin/static',
        )

    :param app: The application object.
    """


@hookspec
def kadi_get_translations_paths():
    """Hook for collecting translation paths.

    The translations path returned by a plugin must be absolute. Note that currently
    translations of the main application and plugins are simply merged together, where
    translations of the main application will always take precedence.
    """


@hookspec
def kadi_register_oauth2_providers(registry):
    """Hook for registering OAuth2 providers.

    Currently, only the authorization code grant is supported. Each provider needs to
    register itself to the given registry provided by the Authlib library using a unique
    name.

    Needs to be used together with :func:`kadi_get_oauth2_providers`.

    :param registry: The OAuth2 provider registry.
    """


@hookspec
def kadi_get_oauth2_providers():
    """Hook for collecting OAuth2 providers.

    Each OAuth2 provider has to be returned as a dictionary containing all necessary
    information about the provider. A provider must at least provide the unique name
    that was also used to register it.

    **Example:**

    .. code-block:: python3

        {
            "name": "my_provider",
            "title": "My provider",
            "website": "https://example.com",
            "description": "The (HTML) description of the OAuth2 provider.",
        }

    Needs to be used together with :func:`kadi_register_oauth2_providers`.
    """


@hookspec
def kadi_get_publication_providers():
    """Hook for collecting publication providers.

    Each publication provider has to be returned as a dictionary containing all
    necessary information about the provider. A provider must at least provide the
    unique name that was also used to register the OAuth2 provider that this provider
    should use.

    **Example:**

    .. code-block:: python3

        {
            "name": "my_provider",
            "description": "The (HTML) description of the publication provider.",
        }

    Needs to be used together with :func:`kadi_register_oauth2_providers` and
    :func:`kadi_get_oauth2_providers`.
    """


@hookspec(firstresult=True)
def kadi_publish_record(record, provider, client, token, task):
    """Hook for publishing a record using a given provider.

    Each plugin has to check the given provider and decide whether it should start the
    publishing process, otherwise it has to return ``None``.

    Needs to be used together with :func:`kadi_get_publication_providers`. Note that the
    hook chain will stop after the first returned result that is not ``None``.

    :param record: The record to publish.
    :param provider: The provider to use for publishing.
    :param client: The OAuth2 client to use for publishing.
    :param token: The OAuth2 token to use for publishing.
    :param task: A :class:`.Task` object that may be provided if this hook is executed
        in a background task.
    """


@hookspec(firstresult=True)
def kadi_get_custom_mimetype(file, base_mimetype):
    """Hook for determining a custom MIME type of a file.

    Each plugin has to check the given base MIME type and decide whether it should try
    determining a custom MIME type or not. Otherwise, it has to return ``None``. The
    returned MIME type should only be based on the content a file actually contains.

    Can be used together with :func:`kadi_get_preview_data`. Note that the hook chain
    will stop after the first returned result that is not ``None``.

    :param file: The :class:`.File` to get the custom MIME type of.
    :param base_mimetype: The base MIME type of the file, based on the actual file
        content, which a plugin can base its decision to return a custom MIME type on.
    """


@hookspec(firstresult=True)
def kadi_get_preview_data(file):
    """Hook for obtaining preview data of a file object to be passed to the frontend.

    Each plugin has to check if preview data should be returned for the given file,
    otherwise it has to return ``None``. The preview data must consist of a tuple
    containing the preview type and the actual preview data used for rendering the
    preview later. To determine the preview data, the given file can be checked for its
    MIME types, both the magic MIME type based on the file's content and the regular
    MIME type.

    Should be used together with :func:`kadi_get_preview_components`. Note that the hook
    chain will stop after the first returned result that is not ``None``.

    :param file: The :class:`.File` to get the preview data of.
    """


@hookspec
def kadi_get_preview_components(file):
    """Hook for collecting frontend components for rendering preview data.

    All more complex previews are currently rendered using Vue.js components, for
    example:

    .. code-block:: js

        Vue.component('my-previewer', {
            // The type of the passed data prop depends on how the preview data is
            // defined in the backend.
            props: {
                data: String,
            },
            // Note the custom delimiters, which are used so they can coexist with
            // Jinja's templating syntax when not using single file components.
            template: `
                <div>{$ data $}</div>
            `
        })

    The script this component resides in has to be loaded before actually using it via a
    custom static route, which a plugin can define by using
    :func:`kadi_register_blueprints`, for example:

    .. code-block:: html

        <script type="application/javascript"
                src="{{ url_for('my_plugin.static', filename='my_previewer.js') }}">
        </script>

        <!-- Check the preview type first before rendering the component. -->
        <div v-if="previewData.type === 'my_type'">
            <!-- Pass the preview data from the backend into the component. -->
            <my-previewer :data="previewData.data"></my-previewer>
        </div>

    Should be used together with :func:`kadi_get_preview_data`.

    :param file: The :class:`.File` the preview data is based of.
    """
