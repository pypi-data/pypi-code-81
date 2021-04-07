#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'mp4ansi',
        version = '0.1.3',
        description = 'A simple ANSI-based terminal emulator that provides multi-processing capabilities.',
        long_description = '[![GitHub Workflow Status](https://github.com/soda480/mp4ansi/workflows/build/badge.svg)](https://github.com/soda480/mp4ansi/actions)\n[![Code Coverage](https://codecov.io/gh/soda480/mp4ansi/branch/main/graph/badge.svg?token=6NTX6LSP7Q)](https://codecov.io/gh/soda480/mp4ansi)\n[![Code Grade](https://www.code-inspector.com/project/20694/status/svg)](https://frontend.code-inspector.com/project/20694/dashboard)\n[![PyPI version](https://badge.fury.io/py/mp4ansi.svg)](https://badge.fury.io/py/mp4ansi)\n\n# mp4ansi #\n\nA simple ANSI-based terminal emulator that provides multi-processing capabilities. MP4ansi will scale execution of a specified function across multiple background processes, where each process is mapped to specific line on the terminal. As the function executes its log messages will automatically be written to the respective line on the terminal. The number of processes along with the arguments to provide each process is specified as a list of dictionaries. The number of elements in the list will dictate the total number of processes to execute (as well as the number of lines in the terminal). The result of each function is written to the respective dictionary element and can be interogated upon completion.\n\nMPansi also supports representing the function execution as a progress bar, you will need to provide an optional config argument containing a dictionary for how to query for the total and count (via regular expressions), see the [examples](https://github.com/soda480/mp4ansi/tree/master/examples) for more detail.\n\nMP4ansi is a subclass of `mpmq`, see [the mpmq PyPi page](https://pypi.org/project/mpmq/) for more information.\n\n### Installation ###\n```bash\npip install mp4ansi\n```\n\n### Examples ###\n\nTo run the samples below you need to install the namegenerator module `pip install namegenerator`.\n\nA simple mp4ansi example:\n```python\nfrom mp4ansi import MP4ansi\nimport uuid, random, namegenerator, time, logging\nlogger = logging.getLogger(__name__)\n\ndef do_work(*args):\n    total = random.randint(400, 600)\n    logger.debug(f\'processing total of {total}\')\n    for _ in range(total):\n        logger.debug(f\'processed {namegenerator.gen()}\')\n        time.sleep(.01)\n    return total\n\nprocess_data = [{} for item in range(8)]\nprint(\'Procesing items...\')\nMP4ansi(function=do_work, process_data=process_data).execute()\nprint(f"Total items processed {sum([item[\'result\'] for item in process_data])}")\n```\n\nExecuting the code above results in the following:\n![example](https://raw.githubusercontent.com/soda480/mp4ansi/master/docs/images/inline-example1.gif)\n\n**Note** the function being executed `do_work` has no context about multiprocessing or the terminal; it simply perform a function on a given dataset. MP4ansi takes care of setting up the multiprocessing, setting up the terminal, and maintaining the thread-safe queues that are required for inter-process communication.\n\nLet\'s update the example to add an identifer for each process and to show execution as a progress bar. To do this we need to provide additonal configuration via the optional `config` parameter. Configuration is supplied as a dictionary; `id_regex` instructs how to query the identifer from the log messages, `id_justify` will right justify the identifer to make things look nice. For the progress bar, we need to specify `total` and `count_regex` to instruct how to query the total and when to count when an item is processed respectively. The value for these settings are specified as regular expressions and will match the function log messages, thus we need to ensure our function has log statements for these.\n\n```python\nfrom mp4ansi import MP4ansi\nimport uuid, random, namegenerator, time, logging\nlogger = logging.getLogger(__name__)\n\ndef do_work(*args):\n    pid = str(uuid.uuid4())\n    logger.debug(f\'processor id {pid[0:random.randint(8, 30)]}\')\n    total = random.randint(400, 600)\n    logger.debug(f\'processing total of {total}\')\n    for _ in range(total):\n        logger.debug(f\'processed {namegenerator.gen()}\')\n        time.sleep(.01)\n    return total\n\nprocess_data = [{} for item in range(8)]\nconfig = {\n    \'id_regex\': r\'^processor id (?P<value>.*)$\',\n    \'id_justify\': True,\n    \'progress_bar\': {\n        \'total\': r\'^processing total of (?P<value>\\d+)$\',\n        \'count_regex\': r\'^processed (?P<value>.*)$\'}}\nprint(\'Procesing items...\')\nMP4ansi(function=do_work, process_data=process_data, config=config).execute()\nprint(f"Total items processed {sum([item[\'result\'] for item in process_data])}")\n```\n\nExecuting the code above results in the following:\n![example](https://raw.githubusercontent.com/soda480/mp4ansi/master/docs/images/inline-example2.gif)\n\nMore [examples](https://github.com/soda480/mp4ansi/tree/master/examples) are included to demonstrate the mp4ansi package. To run the examples, build the Docker image and run the Docker container using the instructions described in the [Development](#development) section.\n\nTo run the example scripts within the container:\n\n```bash\npython examples/example#.py\n```\n\n### Development ###\n\nClone the repository and ensure the latest version of Docker is installed on your development server.\n\n\nBuild the Docker image:\n```sh\ndocker image build \\\n-t \\\nmp4ansi:latest .\n```\n\nRun the Docker container:\n```sh\ndocker container run \\\n--rm \\\n-it \\\n-v $PWD:/mp4ansi \\\nmp4ansi:latest \\\n/bin/sh\n```\n\nExecute the build:\n```sh\npyb -X\n```\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Networking',
            'Topic :: System :: Systems Administration'
        ],
        keywords = '',

        author = 'Emilio Reyes',
        author_email = 'soda480@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/soda480/mp4ansi',
        project_urls = {},

        scripts = [],
        packages = ['mp4ansi'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'mpmq',
            'colorama'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
