"""Spell checking system calls to Hunspell."""

import glob
import os
import subprocess
import tempfile


def hunspell_spellcheck(
    content,
    language_dicts,
    personal_dicts=None,
    encoding=None,
):
    """Call hunspell for spellchecing.

    Args:
        content (str): Content to check for words not included in dictionaries.
        language_dicts (list, str): Language or languages dictionaries (could
            be defined as files) used to check errors.
        personal_dicts (str): Personal dictionary used to exclude valid words
            from being notified as errors.
        encoding (str): Input encoding passed to Hunspell. If is defined, the
            option ``-i`` will be passed to hunspell system call.

    Returns:
        str: Hunspell standard output.
    """
    if not isinstance(language_dicts, str):
        language_dicts = ",".join(language_dicts)

    command = ["hunspell", "-d", language_dicts, "-a"]

    temporal_personal_dict_filename = None
    if personal_dicts:
        if isinstance(personal_dicts, str):
            command.extend(["-p", personal_dicts])
        else:
            if len(personal_dicts) == 1:
                # only one dictionary, no need for composition
                command.extend(["-p", personal_dicts[0]])
            else:
                # compound one dictionary with others content
                hunspellcheck_tempdir = os.path.join(
                    tempfile.gettempdir(),
                    "hunspellcheck",
                )
                if not os.path.isdir(hunspellcheck_tempdir):
                    os.mkdir(hunspellcheck_tempdir)

                temporal_personal_dict_filename = tempfile.NamedTemporaryFile(
                    dir=hunspellcheck_tempdir
                ).name
                if os.path.isfile(temporal_personal_dict_filename):
                    os.remove(temporal_personal_dict_filename)
                os.mknod(temporal_personal_dict_filename)
                for personal_dict_glob in personal_dicts:
                    for personal_dict in glob.glob(personal_dict_glob):
                        with open(
                            temporal_personal_dict_filename, "a"
                        ) as compound_dict_f, open(personal_dict) as partial_dict_f:
                            compound_dict_f.write(f"{partial_dict_f.read()}\n")
                command.extend(["-p", temporal_personal_dict_filename])

    if encoding:
        command.extend(["-i"], encoding)

    response = subprocess.run(
        command,
        universal_newlines=True,
        input=content,
        stdout=subprocess.PIPE,
        check=True,
    )

    if temporal_personal_dict_filename is not None:
        os.remove(temporal_personal_dict_filename)

    return response
