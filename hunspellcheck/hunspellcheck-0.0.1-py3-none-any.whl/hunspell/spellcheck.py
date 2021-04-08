"""Spell checking system calls to Hunspell."""

import subprocess


def hunspell_spellcheck(content, language_dicts, personal_dict=None):
    if not isinstance(language_dicts, str):
        language_dicts = ",".join(language_dicts)

    command = ["hunspell", "-d", language_dicts, "-a"]
    if personal_dict:
        command.extend(["-p", personal_dict])

    return subprocess.run(
        command,
        universal_newlines=True,
        input=content,
        stdout=subprocess.PIPE,
        check=True,
    )
