# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['changelog', 'changelog.cli']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['changelog = changelog.__main__:app']}

setup_kwargs = {
    'name': 'changelog-cmd',
    'version': '0.1.2',
    'description': '',
    'long_description': '# changelog-cmd\n\n![example workflow](https://github.com/jacksmith15/changelog-cmd/actions/workflows/main.yml/badge.svg)\n\nTool for managing a changelog in the style of [Keep a Changelog].\n\n### Features:\n\n- Write new changelog entries in a consistent manner\n- Validate and format your changelog\n- Suggest semantic version of releases based on their contents\n- Write scripts which make automated changes and updates to changelogs, whilst keeping the changelog in a human-readable format\n\n## Installation\n\nRequires Python 3.9 or higher.\n\n```shell\npip install changelog-cmd\n```\n\n## Usage\n\n### Starting a changelog\n\nCreate a changelog named `CHANGELOG.md` in the current directory by running\n\n```shell\nchangelog init --release-link-format=RELEASE_LINK_FORMAT\n```\n\nWhere the `--release-link-format` option specifies how to generate links to a given release, and is given using a Python string format specifier. For example, if you want to link to source on GitHub, this format specifier might be:\n\n- `https://github.com/user/repo/tree/{tag}` - the source code at this release\n- `https://github.com/user/repo/compare/{previous_tag}...{tag}` - a comparison of this release with the one before\n\nOr if you want to link to PyPi, the format might be:\n\n- `https://pypi.org/project/package/{tag}/`\n\nAbove you see the two variables available for substitution:\n- `tag` is the tag of the release\n- `previous_tag` is the tag of the previous release\n\n\n### Finding the changelog\n\nBy default, `changelog` looks for a changelog called `CHANGELOG.md` in the current directory. You can override this by passing a command-line option:\n\n```shell\nchangelog --path path/to/changelog.md ...\n```\n\nOr you can set an environment variable:\n\n```shell\nCHANGELOG_PATH=path/to/changelog.md ...\n```\n\nThe command-line option takes precedence.\n\n### Adding entries to a changelog\n\nAdd an entry to the unreleased section of a changelog:\n\n```shell\nchangelog entry added --message "Description of my change"\n```\n\nYou can replace `added` in the above with any of the following types of entry:\n\n- `added`\n- `changed`\n- `deprecated`\n- `fixed`\n- `removed`\n- `security`\n\nTo specify a change as breaking, simply include the `--breaking` flag:\n\n```shell\nchangelog entry changed --message "Description of a breaking change" --breaking\n```\n\nIf you need to add a missing entry to a past release, you can specify the release tag explicitly:\n\n```shell\nchangelog entry fixed --message "Description of a fix" --tag "0.1.1"\n```\n\n### Cutting a release\n\nWhen you are ready to cut a release, run the following:\n\n```shell\nchangelog release\n```\n\nThis will identify the correct semantic version. Alternatively, you can specify the semantic version bump yourself:\n\n```shell\nchangelog release --bump "major"\n```\n\nOr, if you don\'t use semantic versioning at all, simply specify the tag of the release:\n\n```shell\nchangelog release --tag "2021.r3"\n```\n\n### Formatting and validation\n\nUsing this tool should not preclude manual editing of a changelog. To ensure that manual changes don\'t break conventions, you can use the following two commands in your development workflow:\n\nSimply check that the changelog is still in a recognisable format:\n```shell\nchangelog validate\n```\n\nFormat the changelog in a standard manner:\n```shell\nchangelog format\n```\n\n### Changelog configuration\n\nThis tool stores configuration in the changelog itself. The currently available config fields are:\n\n- `release_link_format` specifies the format for release links\n- `breaking_change_token` specifies the token for breaking changes\n\nCheck the value of a config field via:\n\n```shell\nchangelog config get --field CONFIG_FIELD\n```\n\nAnd set it via\n\n```shell\nchangelog config set --field CONFIG_FIELD --value VALUE\n```\n\n## Development\n\nInstall dependencies:\n\n```shell\npyenv shell 3.9.4  # Or other 3.9.x\npre-commit install  # Configure commit hooks\npoetry install  # Install Python dependencies\n```\n\nRun tests:\n\n```shell\npoetry run inv verify\n```\n\n## Future improvements\n\nThe following is a list of possible future improvements for this tool:\n\n- Support a release-per-change workflow (every change is tagged as a new release)\n- Support configuration of of change types beyond those specified by [Keep a Changelog]\n- Extensions to help interaction with `git`, e.g. merge conflict resolution and/or validation.\n\n## License\nThis project is distributed under the MIT license.\n\n[Keep a Changelog]: http://keepachangelog.com/en/1.0.0/',
    'author': 'Jack Smith',
    'author_email': 'jack.je.smith@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jacksmith15/changelog-cmd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
