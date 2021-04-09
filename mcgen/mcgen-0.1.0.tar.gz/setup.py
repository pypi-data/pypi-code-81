# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcgen', 'mcgen.processors']

package_data = \
{'': ['*']}

extras_require = \
{'colors': ['colorama>=0.4.3,<0.5.0', 'colorlog>=4.2.1,<5.0.0']}

setup_kwargs = {
    'name': 'mcgen',
    'version': '0.1.0',
    'description': "Python utilities for downloading and processing Minecraft's generated data.",
    'long_description': "# mcgen\n\nPython utilities for downloading and processing Minecraft's generated data.\n\n## Requirements\n\n- Python 3.8+\n- Java 11+ (for invoking the Minecraft server's data generator)\n\n## Usage\n\n```bash\npython -m mcgen --help\n```\n\n```\nmcgen [-h] [--jarsdir JARSDIR] [--rawdir RAWDIR] [--outdir OUTDIR] [--version VERSION] [--manifest MANIFEST] [--processors [PROCESSORS [PROCESSORS ...]]] [--log LOG]\n\nDownload the Minecraft server jar for the specified version, invoke the data generator, and process the output.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --jarsdir JARSDIR     Where to download and store server jars. Default: mcgen/jars\n  --rawdir RAWDIR       Where to store the raw server-generated files. Default: mcgen/raw\n  --outdir OUTDIR       Where to write the final processed output. Default: mcgen/out\n  --version VERSION     The server version to download and process. Defaults to latest snapshot.\n  --manifest MANIFEST   Where to fetch the version manifest from. Defaults to Mojang's online copy.\n  --processors [PROCESSORS [PROCESSORS ...]]\n                        Which processors to use in processing the raw server-generated files. Defaults to a pre-defined set of basic processors.\n  --log LOG             The level of verbosity at which to print log messages.\n```\n\n## Processors\n\nProcessors are used to process the raw server-generated data and produce output. They are invoked one after the other, in the order they are defined.\n\nTo provide a custom set of processors, use the `--processors` option like so:\n\n```bash\npython -m mcgen --processors mcgen.processors.split_registries mcgen.processors.summarize_data\n```\n\n### Built-in processors\n\nSeveral built-in processors are provided in [`mcgen.processors`](./mcgen/processors):\n\n- [`convert_json_files`](./mcgen/processors/convert_json_files.py) - Convert json files into another form.\n- [`split_registries`](./mcgen/processors/split_registries.py) - Split `registries.json` into separate files.\n- [`summarize_biomes`](./mcgen/processors/summarize_biomes.py) - Create a summary of biome reports.\n- [`summarize_data`](./mcgen/processors/summarize_data.py) - Create a summary of each vanilla registry.\n- [`write_version_file`](./mcgen/processors/write_version_file.py) - Write the game version to a file.\n\n## Custom processors\n\nProcessors are Python modules containing a function with the following signature:\n\n```python\ndef process(ctx: Context, **options):\n    ...\n```\n\n- `ctx` contains information about the processing context\n- `options` is a key-value mapping of arbitrary data\n",
    'author': 'Arcensoth',
    'author_email': 'arcensoth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Arcensoth/mcgen',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
