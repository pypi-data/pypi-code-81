# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xawsprofile']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['awsprofile = xawsprofile.cli:main']}

setup_kwargs = {
    'name': 'xawsprofile',
    'version': '0.1.9',
    'description': 'AWS profile utility',
    'long_description': '# AWS Profile Utility\n\nThe `awsprofile` utility can be used to simplify working with a large number of profiles. This utility reads from `~/.aws/credentials` and `~/.aws/awsprofile` to list profiles.\n\n## Install\n\n```bash\npip install xawsprofile\n```\n\n## Usage\n\n```bash\n# list profiles\nawsprofile list\n\n# set profile to profile1 and set alias\neval $(awsprofile set profile1 --alias p1)\n\n# list regions\nawsprofile list-regions\n```\n\n## Bash Completion\n\nThis utility includes the following bash completions:\n\n### Select Profile\n\n`ap` (aws profile) - `ap {TAB}{TAB}` then select a profile, hit `{ENTER}`\n\n```bash\n$ ap prof{TAB}{TAB}\nprofile1     profile2\n```\n\n### Select Region\n\n`ar` (aws region) - `ar {TAB}{TAB}`, then select a region, hit `{ENTER}`\n\n```bash\n$ ar us-{TAB}{TAB}\nus-east-1     us-west-1\n```\n\n### Setup Bash Completion\n\n```bash\n# add to your .bash_profile\neval "$(awsprofile completion bash)"\n```\n\n## Commands\n\n### List Profiles\n\n`list` - list profiles\n\n```bash\n$ awsprofile list\nprofile1\nprofile2\n```\n\n### Set Profile\n\n`set` - set the current profile using exported environment variables\n\n```bash\n$ eval(awsprofile set profile1)\n\n# set profile and set alias\n$ eval(awsprofile set profile1 --alias p1)\n```\n\n### List Regions\n\n`list-regions` - list AWS regions\n\n### Configure\n\n`config` - configure awsprofiles\n\nThis currently supports `cwd` to configure the current working directory with a filter.\n\n```bash\n# filter only profiles-* and remove `profiles-` prefix\nawsprofile config cwd --match \'profiles-(.*)`\n```\n\n## Customizations\n\n### Aliases\n\nTo set an alias, update `~/.aws/awsprofile` or use `awsprofile set ... --alias ...` or use `ap {profile} {alias}`.\n\n```bash\neval $(awsprofile set profile1 --alias p1)\n\nap profile1 p1\n```\n\n### Bash Prompt\n\nIf you prefer to update your prompt to display the current AWS profile and region as an interactive prompt, you can update your `PS1` as follows:\n\n```bash\nexport OLDPS1=$PS1\nexport PS1=\'${AWS_PROFILE} (${AWS_DEFAULT_REGION})> \'\n```\n\nYou can reset your prompt after by either running `export PS1=$OLDPS1` to reset the change, or by reloading your shell.\n\n### Naming Rules\n\nTo simplify the profile names, rules can be applied when `awsprofile list` is run.\n\n* global: ~/.aws/awsprofile\n* working directory: {workdir}/.awsprofile (this overrides anything in global)\n\n```text\n# rename blah-* by removing "blah-" (ex: blah-test would be just test)\n[naming cleanup-blah]\nmatch = blah-(.*)\nreplace = \\1\n\n# hide test-*\n[naming hide-test]\nmatch = test-(.*)\nvisible = false\n\n# hide all but test-*\n[naming hide-others]\nmatch = test-(.*)\nnegate = true\nvisible = false\n\n# only applies to {workdir}/.awsprofile\n[naming]\ninherit_global = true\n```\n\n### Tips\n\n* `awsprofile config cwd --match \'profiles-(.*)` will setup the current working directory to filter only `profiles-*` as well as strip `profiles-` from the profile names. This generates a `.awsprofile` in the current working directory.',
    'author': 'Daniel Clayton',
    'author_email': 'dclayton@godaddy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
