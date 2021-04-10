# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['suzieq',
 'suzieq..ropeproject',
 'suzieq.cli',
 'suzieq.cli.sqcmds',
 'suzieq.db',
 'suzieq.db.parquet',
 'suzieq.engines',
 'suzieq.engines.pandas',
 'suzieq.gui',
 'suzieq.gui.pages',
 'suzieq.poller',
 'suzieq.poller.nodes',
 'suzieq.poller.services',
 'suzieq.restServer',
 'suzieq.sqobjects',
 'suzieq.utilities']

package_data = \
{'': ['*'],
 'suzieq': ['config/*',
            'config/etc/*',
            'config/schema/*',
            'config/textfsm_templates/*'],
 'suzieq.gui': ['images/*', 'notebooks/*'],
 'suzieq.gui.pages': ['help/Path.md']}

install_requires = \
['PyYAML',
 'aiofiles',
 'aiohttp==3.7.4',
 'async-timeout',
 'asyncssh==2.4.2',
 'bcrypt>=3.2.0,<4.0.0',
 'dateparser>=1.0.0,<2.0.0',
 'faker>=4.1.1,<5.0.0',
 'fastapi>=0.61.1,<0.62.0',
 'fido2>=0.9.1,<0.10.0',
 'graphviz>=0.15,<0.16',
 'jsonpath-ng>=1.5.1,<2.0.0',
 'matplotlib>=3.2.2,<4.0.0',
 'netconan>=0.11.2,<0.12.0',
 'networkx>=2.4,<3.0',
 'pandas==1.2.3',
 'prompt-toolkit>2',
 'pyarrow==3.0.0',
 'python-nubia==0.2b5',
 'streamlit>=0.79.0,<0.80.0',
 'tabulate>=0.8.7,<0.9.0',
 'textfsm',
 'uvicorn>=0.11.8,<0.12.0',
 'uvloop']

entry_points = \
{'console_scripts': ['sq-anonymizer = '
                     'suzieq.utilities.sq_anonymizer:anonymizer_main',
                     'sq-coalescer = '
                     'suzieq.utilities.sq_coalescer:coalescer_main',
                     'sq-poller = suzieq.poller.sq_poller:poller_main',
                     'sq-rest-server = '
                     'suzieq.restServer.sq_rest_server:rest_main',
                     'suzieq-cli = suzieq.cli.sq_cli:cli_main',
                     'suzieq-gui = suzieq.gui.sq_gui:gui_main']}

setup_kwargs = {
    'name': 'suzieq',
    'version': '0.11.1',
    'description': 'A framework and application for network observability',
    'long_description': "![integration-tests](https://github.com/netenglabs/suzieq/workflows/integration-tests/badge.svg)\n\n# Suzieq -- Healthier Networks Through Network Observability\n\nWould you like to be able to easily answer trivial questions such as how many unique prefixes are there in your routing table, or how many MAC addresses are there in the MAC tables across the network? How about more difficult questions, such as what changes did your routing table see between 10 pm and midnight last night, or which of your nodes have been up the longest, or which BGP sessions have had the most routing updates? How about being able to answer if your OSPF (or BGP) sessions are working correctly, or is all well with your EVPN? How about a quick way to determine the amount of ECMP at every hop between two endpoints? Do you wish you could easily validate the configuration you deployed across your network?\n\nDo you login to every network node you have to figure out answers to a questions like these? Do you then struggle to piece the information together into a consistent whole across the various formats provided by various vendors? Do you wish you had an **open source, multi-vendor** tool that could help you answer questions like these and more?\n\nIf you answered yes to one or more of these questions, then Suzieq is a tool that we think will be interesting to you.  **Suzieq helps you find things in your network.**\n\n**Suzieq** is both a framework and an application using that framework, that is focused on **improving the observability of your network**.  We define observability as the ability of a system to answer either trivial or complex questions that you pose as you go about operating your network. How easily you can answer your questions is a measure of how good the system's observability is. A good observable system goes well beyond monitoring and alerting. Suzieq is primarily meant for use by network engineers and designers.\n\nSuzieq does multiple things. It [collects](https://suzieq.readthedocs.io/en/latest/poller/) data from devices and systems across your network. It normalizes the data and then stores it in a vendor independent way. Then it allows analysis of that data. With the applications that we build on top of the framework we want to demonstrate a different and more systematic approach to thinking about networks. We want to show how useful it is to think of your network holistically.\n\n## Quick Start\n\n### Using Docker Container\nWe want to make it as easy as possible for you to start engaging with Suzieq, so we have a demo that has data in including the the iamge.\n\n* `docker run -it -p 8501:8501 --name suzieq netenglabs/suzieq-demo`\n* `suzieq-cli` for the CLI OR\n* `suzieq-gui` for the GUI. Connect to http://localhost:8501 via the browser to access the GUI\n\nWhen you're within the suzieq-cli, you can run ```device unique columns=namespace``` to see the list of different scenarios, we've gathered data for.\n\nAdditional information about running the analyzer (suzieq-cli) is available via the official documentation page.\n\nTo start collecting data for your network, create an inventory file to gather the data from following the instructions [here](https://suzieq.readthedocs.io/en/latest/poller/). Decide the directory where the data will be stored (ensure you have sufficient available space if you're going to be running the poller, say 100 MB at least). Lets call this dbdir. Now launch the suzieq docker container as follows:\n\n* ```docker run -it -vdbdir:/suzieq/parquet --name sq-poller netenglabs/suzieq```\n* Connect to the container via ```docker attach sq-poller```\n* Launch the poller with the appropriate options. For example, ```sq-poller -D inventory.yml -k``` where mydatacenter is the name of the namespace where the data associated with the inventory is storedand inventory.yml is the inventory file in Suzieq poller native format (Use -a if you're using Ansible inventory file format).\n\n### Using Python Packaging\n\nIf you don't want to use docker container or cannot use a docker container, an alternative approach is to install Suzieq as a python package. It is **strongly** recommended to install suzieq inside a virtual environment. If you already use a tool to create and manage virtual environments, you can skip the step of creating a virtual envirobment below.\n\nSuzieq requires python version 3.7.1 at least, and has been tested with python versions 3.7 and 3.8. It has not been tested to work on Windows. Use Linux (recommended) or macOS. To create a virtual environment, in case you haven't got a tool to create one, type:\n```\npython -m venv suzieq\n```\nThis creates a directory called suzieq and all suzieq related info is stored there. Switch to that directory and activate the virtual environment with:\n```\nsource activate\n```\nNow the virtual environment is alive and you can install suzieq. To install suzieq, execute:\n```\npip install suzieq\n```\n\nOnce the command completes, you have the main programs of suzieq available for use:\n\n* sq-poller: For polling the devices and gathering the data\n* suzieq-gui: For launching the GUI\n* suzieq-cli: For running the CLI\n* sq-rest-server: For running the REST API server\n\n[The official documentation is at suzieq.readthedocs.io](https://suzieq.readthedocs.io/en/latest/) \n\n# Analysis\n\nSuzieq supports Analysis using CLI, GUI, REST API, and python objects. For the most part they are equivalent, though with the GUI we have combined the output of multiple commands of the CLI into one page.\n\nThe GUI has a  status page to let you know what the status of entitites in your network.\n![Suzieq GUI status](images/status.png)\n\nThe Xplore page lets you dive into what is in your network. ![Explore device](images/devices-gui.png)\n\nThe CLI supports the same kind of analysis as the explore page. ![CLI device](images/devices-cli.png)\n\n[More examples of the CLI can be seen in the docs and blog posts we've created.](https://suzieq.readthedocs.io/en/latest/analyzer/)\n\n## Path\n\nSuzieq has the ability to show the path between two IP addresses, including the ability to show the path through EVPN overlay. You can use this to see each of the paths from a source to a destination and to see if you have anything asymetrical in your paths. ![GUI PATH](images/path-gui.png)\n\n## Asserts\n\nOne of Suzieqs powerful capabilities are asserts, which are statements that should be true in the network. We've only just started on asserts; what Suzieq has now only demonstrates it's power, there's a lot more to be added in this space. ![interfaces assert](images/interfaces-assert.png)\n\n# Suzieq Data\n\n**Suzieq supports gathering data from Cumulus, EOS, IOSXR, JunOS(QFX, MX, EX, SRX supported), NXOS and SONIC routers, and Linux servers.** Suzieq gathers:\n\n* Basic device info including serial number, model, version, platform etc.\n* Interfaces\n* LLDP\n* MAC address table (VPLS MAC table for Junos MX)\n* MLAG\n* Routing table\n* ARP/ND table\n* OSPFv2\n* BGP\n* EVPN VNI info\n\nWe're addding support for more platforms and features with every release. \n\nWe're also looking for collaborators to help us make Suzieq a truly useful multi-vendor, open source platform for observing all aspects of networking. Please read the [collaboration document](./CONTRIBUTING.md) for ideas on how you can help.\n\n# Latest Release\n\nThe latest release is 0.11.0 and the official release notes are [here](https://suzieq.readthedocs.io/en/latest/release-notes/).\n\n# Engage\n\nYou can join the conversation via [slack](https://join.slack.com/t/netenglabs/shared_invite/zt-g64xa6lc-SeP2OAj~3uLbgOWJniLslA). Send email to Dinesh or Justin with the email address to send the Slack invitation to.\n\n# Additional Documentation\n\nWe've done some blogging about Suzieq:\n\n* [Introducing Suzieq](https://elegantnetwork.github.io/posts/Suzieq/)\n* [10ish ways to explore your network with Suzieq](https://elegantnetwork.github.io/posts/10ish_ways_to_explore_your_network_with_Suzieq/)\n* [Questions to Suzieq](https://elegantnetwork.github.io/posts/10qa-suzieq/)\n* [Time in Suzieq](https://elegantnetwork.github.io/posts/time-suzieq/)\n\n# Suzieq Priorities\n\nWe don't have a roadmap, but we do have a list of our [priorities](https://github.com/netenglabs/suzieq/blob/master/docs/2020-priority.md). We mix this with the [issues reported](https://github.com/netenglabs/suzieq/issues).\n",
    'author': 'suzieq dev team',
    'author_email': None,
    'maintainer': 'suzieq dev team',
    'maintainer_email': None,
    'url': 'https://www.stardustsystems.net/suzieq/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.7.1,<3.9',
}


setup(**setup_kwargs)
