# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daml_dit_ddit']

package_data = \
{'': ['*']}

install_requires = \
['GitPython==3.1.12',
 'PyGithub==1.54.1',
 'dacite',
 'daml-dit-api==0.3.3',
 'pex==2.1.30',
 'pyyaml>=5,<6']

entry_points = \
{'console_scripts': ['ddit = daml_dit_ddit:main']}

setup_kwargs = {
    'name': 'daml-dit-ddit',
    'version': '0.4.9',
    'description': 'DABL DIT File Tool',
    'long_description': "daml-dit-ddit\n====\n\n`ddit` is a command line tool, written in Python, to streamline and\nautomate the process of building composite artifacts for\n[project:DABL](https://www.projectdabl.com/). DABL stores composite\nartifacts in [DIT files](https://github.com/digital-asset/daml-dit-api),\nwhich aggregate metadata alongside multiple deployable entities in a\nsingle file. DABL uses these to store application deployments as well\nas integrations.\n\n# Installing `ddit`\n\n`ddit` is a Python executable built using [PEX](https://github.com/pantsbuild/pex),\nand distributed via the [PyPI](https://pypi.org/project/daml-dit-ddit/) package index.\n\nGiven a Python installation of version 3.7 or later, `ddit` can be installed using `pip3`\n\n```sh\n$ pip3 install daml-dit-ddit\n```\n\nOnce installed, verify `ddit` by launching it without arguments:\n\n```sh\n$ ddit\nusage: ddit [-h] [--verbose] {build,ditversion,genargs,inspect,release,show,targetname} ...\n\npositional arguments:\n  {build,ditversion,genargs,inspect,release,show,targetname}\n                        subcommand\n    build               Build a DIT file.\n    ditversion          Print the current version in dabl-meta.yaml\n    genargs             Write a template integration argfile to stdout\n    inspect             Inspect the contents of a DIT file.\n    release             Tag and release the current DIT file.\n    show                Verify and print the current metadata file.\n    targetname          Print the build target filename to stdout\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --verbose             Turn on additional logging.\n2021-02-03T19:24:31-0500 [ERROR] (ddit) Fatal Error: Subcommand missing.\n```\n\n# Using `ddit`\n\n`ddit` is used to build two major categories of DAR files:\napplications and integrations. Applications are simple composites of\none or more distinct sub-artifacts. This is useful to deploy, for\nexample, a DAML model alongside the Python Bots and UI code composing\nthe rest of the application. When building these sorts of DIT files,\n`ddit` primarily serves to assemble packages out of components built\nby other build processes. Put another way, `ddit` won't build your\nuser interface itself, it has to be built before `ddit` can package\nit into a DIT file.\n\nFor examples of what this looks like in practice, please see one of\nseveral sample applications available through DABL:\n\n* <https://github.com/digital-asset/dablchat>\n* <https://github.com/digital-asset/dablchess>\n* <https://github.com/OpenSaaSame/board>\n\nThese are all built using Makefiles that delegate to `ddit` to manage\npackaging and release. Make runs the overall build process using `ddit\nditversion` and `ddit targetname` to parse out version and name\ninformation from `dabl-meta.yaml`, `ddit build` to package the DIT\nfile, and `ddit release` to release that DIT file to Github.\n\n## Specific support for DAML\n\n`ddit` is integrated into the DAML ecosystem and will, by default,\ntreat the the root build directory as a DAML project directory if\nthere is a `daml.yaml` file in the root. As part of `ddit build`,\n`ddit` will recursively invoke the\n[DAML SDK's](https://docs.daml.com/getting-started/installation.html)\n`daml build` command to build the DAML model used by the DIT file.\nIf it is necessary to take more fine grained control over the model\nbuild process, this can be disabled by specifying `--skip-dar-build`.\n\nNote also that `ddit` will not rebuild a DAR file that already exists\nunless `--force` is specified. This is intended to make it easier to\nkeep a given DAR file stable across multiple releases of the same DIT\nfile. If the model is stable, the DAR itself should also be stable.\n\n# Building integrations\n\nIntegration DIT files differ from applications in that they contain\ncode that runs within the DABL cluster that has access to both a\nledger and the external network. Because of these elevated access\nrights, specific permissions are required to deploy these DIT files to\nDABL, and these DIT files must be built using the `--integration` flag\npassed to `ddit build`.\n\nWhen running in integration mode, The DIT file build directory is\nconsidered to be a Python project. Python dependencies are specified\nin `requirements.txt`, Python source code is under `src`, and the\nproject is built using an instance of [PEX](https://github.com/pantsbuild/pex)\nthat is internal to `ddit` itself.\n\nIntegration DIT files are also allowed (and required) to have an\n`integration_types` section in their `dabl-meta.yaml` specifying the\nintegrations supported by the DIT file. This is enforced by `ddit`:\n`--integration` mode is required to build DIT files that specify\nintegration types.\n",
    'author': 'Mike Schaeffer',
    'author_email': 'mike.schaeffer@digitalasset.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/digital-asset/daml-dit-ddit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
