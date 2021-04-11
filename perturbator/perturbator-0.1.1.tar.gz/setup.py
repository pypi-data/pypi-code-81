# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['perturbator',
 'perturbator.commands',
 'perturbator.language_parser',
 'perturbator.support_modules']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.0.3,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'shortuuid>=1.0.1,<2.0.0',
 'textX>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['perturbator = perturbator.perturbator:main']}

setup_kwargs = {
    'name': 'perturbator',
    'version': '0.1.1',
    'description': 'Tool to apply change patterns on Business Process Models',
    'long_description': "# perturbator\n\nTool to apply change patterns to your Business Process Models\n\n## Dependencies:\n`python3`\n`poetry`\n`click`\n`shortuuid`\n`textx`\n\n## Setup\n`poetry install`\n\n`poetry run perturbator`\n\n## Insert Element\n### Documentation\n`poetry run perturbator insert-element --help`\n\n### Options:\n\n  `--insert-to`     BPMN File Path in which element has to be inserted      [required]\n\n  `--element-type`   Type of element to be inserted                         [required]\n\n  `--output-file`   Path of BPMN file in which to output                    [required]\n\n  `--insert-at`     ID of the FLOW where the process has to be inserted     [required]\n\n### Sample Command:\n`poetry run perturbator insert-element --insert-to ~/Desktop/input1.bpmn --element-type task --insert-at flow11  --output-file ~/Desktop/output.bpmn`\n\n\n## Delete/Skip Element\n### Documentation\n`poetry run perturbator delete-element --help`\n\n### Options:\n\n  `--delete-from`   BPMN File Path from which element has to be skipped     [required]\n\n  `--element-id`    ID of Element to be deleted                             [required]\n\n  `--output-file`   Path of BPMN file in which to output                    [required]\n\n### Sample Command:\n`poetry run perturbator delete-element --delete-from ~/Desktop/input1.bpmn --element-id task11 --output-file ~/Desktop/output.bpmn`\n\n\n## Insert Process Fragment (Serial)\n### Documentation\n`poetry run perturbator insert-process-fragment-serial --help`\n\n### Options:\n\n  `--insert-to`     BPMN File Path in which process has to be inserted      [required]\n\n  `--insert-from`   BPMN File Path from which process has to be inserted    [required]\n\n  `--output-file`   Path of BPMN file in which to output                    [required]\n\n  `--insert-at`     ID of the FLOW where the process has to be inserted     [required]\n\n### Sample Command:\n`poetry run perturbator insert-process-fragment-serial --insert-to ~/Desktop/input1.bpmn --insert-at flow12 --insert-from ~/Desktop/input2.bpmn --output-file ~/Desktop/output.bpmn `\n\n\n## Insert Process Fragment (Parallel Branch)\n### Documentation\n`poetry run perturbator insert-process-fragment-parallel --help`\n\n### Options:\n\n  `--insert-to`     BPMN File Path in which process has to be inserted      [required]\n\n  `--insert-from`   BPMN File Path from which process has to be inserted    [required]\n\n  `--output-file`   Path of BPMN file in which to output                    [required]\n\n  `--branch-start`  ID of the FLOW where the branching starts               [required]\n\n  `--branch-end`    ID of the FLOW where the branching starts               [required]\n\n### Sample Command:\n`poetry run perturbator insert-process-fragment-parallel --insert-to ~/Desktop/input1.bpmn --insert-from ~/Desktop/input2.bpmn --output-file ~/Desktop/output.bpmn --branch-start flow11 --branch-end flow13`\n\n\n## Insert Process Fragment (Conditional Branch)\n### Documentation\n`poetry run perturbator insert-process-fragment-conditional --help`\n\n### Options:\n\n  `--insert-to`     BPMN File Path in which process has to be inserted      [required]\n\n  `--insert-from`   BPMN File Path from which process has to be inserted    [required]\n\n  `--output-file`   Path of BPMN file in which to output                    [required]\n\n  `--branch-start`  ID of the FLOW where the branching starts               [required]\n\n  `--branch-end`    ID of the FLOW where the branching starts               [required]\n\n### Sample Command:\n`poetry run perturbator insert-process-fragment-conditional --insert-to ~/Desktop/input1.bpmn --insert-from ~/Desktop/input2.bpmn --output-file ~/Desktop/output.bpmn --branch-start flow11 --branch-end flow13`\n\n\n## Delete/Skip Process Fragment\n### Documentation\n`poetry run perturbator delete-process-fragment --help`\n\n### Options:\n\n  `--delete-from`   BPMN File Path from which process fragment has to be deleted    [required]\n\n  `--output-file`   Path of BPMN file in which to output                            [required]\n\n  `--branch-start`  ID of the FLOW where the branching starts                       [required]\n\n  `--branch-end`    ID of the FLOW where the branching starts                       [required]\n\n### Sample Command:\n`poetry run perturbator delete-process-fragment --delete-from ~/Desktop/input1.bpmn  --output-file ~/Desktop/output.bpmn --branch-start flow11 --branch-end flow13`\n\n## Run commands in batches\nAdd commands in a text format in any text file and execute to trigger multiple steps in one go\n\n### Sample Command:\n`poetry run perturbator execute-from-file --command-file ~/Desktop/commands.txt`\n\n### Format of commands in file:\n\n```\ninsert 'task' to process in file '~/Desktop/input1.bpmn' at flow 'flow11' and output in '~/Desktop/output.bpmn'\ndelete element with id 'task11' from process in file '~/Desktop/output.bpmn' and output in '~/Desktop/output.bpmn'\n\n\nserial insert process from '~/Desktop/input2.bpmn' to process in file '~/Desktop/output.bpmn' at flow 'flow12' and output in '~/Desktop/output.bpmn'\nconditionally insert process from '~/Desktop/input2.bpmn' to process in file '~/Desktop/input1.bpmn' between 'flow11' and 'flow13' and output in '~/Desktop/output.bpmn'\nparallel insert process from '~/Desktop/input2.bpmn' to process in file '~/Desktop/input1.bpmn' between 'flow11' and 'flow13' and output in '~/Desktop/output.bpmn'\ndelete process fragment from process in file '~/Desktop/input1.bpmn' between 'flow11' and 'flow13' and output in '~/Desktop/output.bpmn'\n```\n",
    'author': 'Zohaib Ahmed Butt',
    'author_email': 'zohaibahmedbutt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
