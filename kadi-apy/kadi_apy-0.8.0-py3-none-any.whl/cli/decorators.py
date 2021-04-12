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
import sys
from functools import wraps

import click
from requests.exceptions import MissingSchema
from requests.exceptions import SSLError
from xmlhelpy import Integer
from xmlhelpy import option

from kadi_apy.cli.lib.users import CLIUser
from kadi_apy.globals import resource_mapping
from kadi_apy.lib.core import KadiManager
from kadi_apy.lib.exceptions import KadiAPYConfigurationError
from kadi_apy.lib.exceptions import KadiAPYException
from kadi_apy.lib.exceptions import KadiAPYInputError


def apy_command(func):
    """Decorator to handle the default arguments and exceptions of an APY command."""

    option(
        "instance",
        char="I",
        description="Name of a Kadi instance defined in the config file.",
    )(func)

    @wraps(func)
    def decorated_command(instance, *args, **kwargs):

        try:
            kwargs["manager"] = KadiManager(instance=instance)
        except KadiAPYConfigurationError as e:
            click.echo(e, err=True)
            sys.exit(1)

        try:
            func(*args, **kwargs)
        except KadiAPYException as e:
            click.echo(e, err=True)
            sys.exit(1)
        except SSLError as e:
            click.echo(e, err=True)
            click.echo(
                "Use 'verify = False' in the config file to skip verifying the SSL/TLS"
                " certificate of the host (not recommended) or include a path to"
                " certificates of trusted CAs in the config file via"
                " 'ca_bundle = /path/to/certfile'."
            )
            sys.exit(1)
        except MissingSchema as e:
            click.echo(e, err=True)
            click.echo(
                "Please check the host information since the URL schema (e.g. http or"
                " https) is missing."
            )
            sys.exit(1)

    return decorated_command


def id_identifier_options(
    class_type, keep_manager=False, helptext=None, name=None, required=True, char=None
):
    r"""Decorator to handle the common ID and identifier options of commands.

    :param class_type: The resource type defined either as string or class.
    :param keep_manager: (optional) Whether to keep the manager for further use.
    :param helptext: (optional) Text to describe the input.
    :param name: (optional) Name to better describe the input.
    :param required: (optional) Whether the parameter is required.
    :param char: (optional) Char for the options.
    """

    def decorator(func):

        if isinstance(class_type, str):
            resource = resource_mapping(class_type)
        else:
            resource = class_type

        help_id = f"ID of the {resource.name}"
        if helptext:
            help_id = f"{help_id} {helptext}"

        help_identifier = f"Identifier of the {resource.name}"
        if helptext:
            help_identifier = f"{help_identifier} {helptext}"

        if name is None:
            text_option = f"{resource.name}-id"
            if not char:
                char_option_1 = f"{resource.name[0].lower()}"
        else:
            text_option = f"{resource.name}-id-{name.lower()}"
            if not char:
                char_option_1 = f"{name[0].lower()}"

        if char:
            char_option_1 = f"{char[0].lower()}"
            char_option_2 = f"{char[0].upper()}"

        option(
            text_option,
            char=char_option_1,
            description=help_id,
            param_type=Integer,
            default=None,
        )(func)

        if name is None:
            text_option = f"{resource.name}-identifier"
            if not char:
                char_option_2 = f"{resource.name[0].upper()}"
        else:
            text_option = f"{resource.name}-identifier-{name.lower()}"
            if not char:
                char_option_2 = f"{name[0].upper()}"

        option(
            text_option,
            char=char_option_2,
            description=help_identifier,
            default=None,
        )(func)

        @wraps(func)
        def decorated_command(manager, *args, **kwargs):
            if name is None:
                text_id = f"{resource.name}_id"
                text_identifier = f"{resource.name}_identifier"
            else:
                text_id = f"{resource.name}_id_{name.lower()}"
                text_identifier = f"{resource.name}_identifier_{name.lower()}"

            item_id = kwargs[f"{text_id}"]
            item_identifier = kwargs[f"{text_identifier}"]

            if (item_id is None and item_identifier is None and required) or (
                item_id is not None and item_identifier is not None
            ):
                text = (
                    f"Please specify either the id or the identifier of the"
                    f" {resource.name}"
                )
                if helptext:
                    text = f"{text} {helptext}"
                click.echo(f"{text}.")
                sys.exit(1)

            # Init the item either by the id or the identifier.
            # The item is directly passed to the function as e.g. record in case of
            # records or {name} if a name is given. If no information is given, None is
            # returned.
            if item_id is not None or item_identifier is not None:
                item = resource(manager=manager, identifier=item_identifier, id=item_id)
            else:
                item = None

            if name is None:
                kwargs[f"{resource.name}"] = item
            else:
                kwargs[f"{name.lower()}"] = item

            del kwargs[f"{text_id}"]
            del kwargs[f"{text_identifier}"]

            if keep_manager:
                kwargs["manager"] = manager

            func(*args, **kwargs)

        return decorated_command

    return decorator


def user_id_options(helptext=None, required=True, keep_manager=False):
    """Decorator to handle options to identify a user."""

    def decorator(func):

        description = "ID of the user"
        if helptext:
            description = f"{description} {helptext}"

        option(
            "user",
            char="u",
            description=description,
            default=None,
            param_type=Integer,
        )(func)

        description = "Username of the user"
        if helptext:
            description = f"{description} {helptext}"

        option(
            "username",
            char="U",
            description=description,
            default=None,
        )(func)

        description = "Identity type of the user"
        if helptext:
            description = f"{description} {helptext}"

        option(
            "identity-type",
            char="D",
            description=description,
            default="ldap",
        )(func)

        @wraps(func)
        def decorated_command(user, username, identity_type, manager, *args, **kwargs):

            if user is None and username is None:
                if required:
                    raise KadiAPYInputError(
                        "Please specify the user via id or username and identity type."
                    )
                kwargs["user"] = None

            else:
                kwargs["user"] = CLIUser(
                    manager,
                    id=user,
                    username=username,
                    identity_type=identity_type,
                    **kwargs,
                )

            if keep_manager:
                kwargs["manager"] = manager

            func(*args, **kwargs)

        return decorated_command

    return decorator


def file_id_options(helptext=None, required=True, name=None, char=None):
    r"""Decorator to handle options to identify a file of a record.

    :param helptext: (optional) Text to describe the input.
    :param required: (optional) Whether the parameter is required.
    :param name: (optional) Name to better describe the input.
    :param char: (optional) Char for the options.
    """

    def decorator(func):

        description = "Name of the file"
        if helptext:
            description = f"{description} {helptext}"

        if name is None:
            text_option = "file-name"
            if not char:
                char_option_1 = "n"
        else:
            text_option = f"{name}-name"
            if not char:
                char_option_1 = f"{name[0].lower()}"

        if char:
            char_option_1 = f"{char[0].lower()}"
            char_option_2 = f"{char[0].upper()}"

        option(
            text_option,
            char=char_option_1,
            description=description,
            default=None,
        )(func)

        description = "ID of the file"
        if helptext:
            description = f"{description} {helptext}"

        if name is None:
            text_option = "file-id"
            if not char:
                char_option_2 = "i"
        else:
            text_option = f"{name}-id"
            if not char:
                char_option_2 = f"{name[0].upper()}"

        option(
            text_option,
            char=char_option_2,
            description=description,
            default=None,
        )(func)

        @wraps(func)
        def decorated_command(*args, **kwargs):

            if name is None:
                text_id = "file_id"
                text_name = "file_name"
            else:
                text_id = f"{name}_id"
                text_name = f"{name}_name"

            file_id = kwargs[f"{text_id}"]
            file_name = kwargs[f"{text_name}"]

            if required:
                if (file_name is None and file_id is None) or (
                    file_name is not None and file_id is not None
                ):
                    text = "Please specify either the name or the id of the file"
                    if helptext:
                        text = f"{text} {helptext}"
                    click.echo(f"{text}.")
                    sys.exit(1)

            if file_name:
                record = kwargs["record"]
                kwargs[f"{text_id}"] = record.get_file_id(file_name)
            else:
                kwargs[f"{text_id}"] = file_id

            del kwargs[f"{text_name}"]

            func(*args, **kwargs)

        return decorated_command

    return decorator
