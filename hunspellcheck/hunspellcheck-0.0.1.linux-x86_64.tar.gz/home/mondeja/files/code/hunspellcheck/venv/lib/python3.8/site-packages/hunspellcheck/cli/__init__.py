"""CLI utilities writing spell checkers."""

import warnings

from hunspellcheck.cli.files import FilesOrGlobsAction
from hunspellcheck.cli.languages import create_hunspell_valid_dictionary_action
from hunspellcheck.cli.personal_dict import PersonalDictionaryAction
from hunspellcheck.cli.version import DEFAULT_VERSION_TEMPLATE, render_version_template


def extend_argument_parser(
    parser,
    version=False,
    version_prog=None,
    version_number=None,
    hunspell_version=True,
    ispell_version=True,
    version_template=DEFAULT_VERSION_TEMPLATE,
    version_template_kwargs={},
    version_args=["--version"],
    version_kwargs={},
    files=True,
    files_kwargs={},
    languages=True,
    languages_args=["-l", "--language"],
    languages_kwargs={},
    negotiate_languages=True,
    personal_dict=True,
    personal_dict_args=["-p", "--personal-dict"],
    personal_dict_kwargs={},
):
    if version:
        version_string = render_version_template(
            version_template,
            version_template_kwargs,
            version_prog=version_prog if version_prog is not None else parser.prog,
            version_number=version_number,
            hunspell_version=hunspell_version,
            ispell_version=ispell_version,
        )

        if version_string:
            _version_kwargs = {"action": "version", "version": version_string}
            _version_kwargs.update(version_kwargs)

            parser.add_argument(*version_args, **_version_kwargs)
        else:
            readable_version_option = "/".join(version_args)
            warnings.warn(
                f"'{readable_version_option}' option not added because version"
                " string is empty!"
            )

    if files:
        _files_kwargs = {
            "nargs": "*",
            "type": str,
            "dest": "files",
            "metavar": "FILES",
            "help": "Files and/or globs to check.",
            "action": FilesOrGlobsAction,
        }
        _files_kwargs.update(files_kwargs)
        parser.add_argument(**_files_kwargs)

    if languages:
        _languages_kwargs = {
            "type": str,
            "required": True,
            "metavar": "LANGUAGE",
            "dest": "languages",
            "help": "Language to check, you'll have to install the"
            " corresponding hunspell dictionary.",
        }

        _languages_kwargs["action"] = create_hunspell_valid_dictionary_action(
            negotiate_languages=negotiate_languages,
        )
        _languages_kwargs.update(languages_kwargs)
        parser.add_argument(*languages_args, **_languages_kwargs)

    if personal_dict:
        _personal_dict_kwargs = {
            "type": str,
            "required": False,
            "metavar": "PERSONAL_DICTIONARY",
            "dest": "personal_dict",
            "help": "Additional dictionary to extend the words to exclude.",
            "action": PersonalDictionaryAction,
            "nargs": 1,
            "default": None,
        }
        _personal_dict_kwargs.update(personal_dict_kwargs)
        parser.add_argument(*personal_dict_args, **_personal_dict_kwargs)
