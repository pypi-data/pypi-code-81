# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['goth',
 'goth.api_monitor',
 'goth.assertions',
 'goth.runner',
 'goth.runner.cli',
 'goth.runner.container',
 'goth.runner.download',
 'goth.runner.probe']

package_data = \
{'': ['*'],
 'goth': ['default-assets/*',
          'default-assets/docker/*',
          'default-assets/keys/*',
          'default-assets/provider/*',
          'default-assets/web-root/*']}

install_requires = \
['aiohttp==3.7.3',
 'ansicolors>=1.1.0,<2.0.0',
 'docker-compose>=1.29,<2.0',
 'docker>=5.0,<6.0',
 'dpath>=2.0,<3.0',
 'func_timeout==4.3.5',
 'ghapi>=0.1.16,<0.2.0',
 'mitmproxy>=5.3,<6.0',
 'pyyaml>=5.4,<6.0',
 'transitions>=0.8,<0.9',
 'typing_extensions==3.7.4.3',
 'urllib3>=1.26,<2.0',
 'ya-aioclient>=0.5,<0.6']

setup_kwargs = {
    'name': 'goth',
    'version': '0.2.2',
    'description': 'Golem Test Harness - integration testing framework',
    'long_description': '# Golem Test Harness\n\n![codestyle](https://github.com/golemfactory/goth/workflows/codestyle/badge.svg?event=push)\n![test](https://github.com/golemfactory/goth/workflows/test/badge.svg?event=push)\n\n`goth` is an integration testing framework intended to aid the development process of [`yagna`](https://github.com/golemfactory/yagna) itself, as well as apps built on top of it.\n\n## Running the tests locally\n\n### Python setup\n\n#### Python 3.8\nThe test runner requires Python 3.8+ to be installed on the system. You can check your currently installed Python version by running:\n```\npython3 --version\n```\n\nIf you don\'t have Python installed, download the appropriate package and follow instructions from the [releases page](https://www.python.org/downloads/).\n\n#### Project installation\n`goth` is not (yet) available as a standalone package, therefore you will need to set up its development environment in order to use it.\n\n##### poetry\n`goth` uses [`poetry`](https://python-poetry.org/) to manage its dependencies and provide a runner for common tasks (e.g. running E2E tests).\nIf you don\'t have `poetry` available on your system then follow its [installation instructions](https://python-poetry.org/docs/#installation) before proceeding.\nVerify your installation by running:\n```\npoetry --version\n```\n\n##### project dependencies\nTo install the project\'s dependencies run:\n```\npoetry install\n```\n\n### Docker setup\n\n#### Docker Engine\nThe tests are performed on live Yagna nodes running in an isolated network. Currently, this setup is achieved by running a number of Docker containers locally using Docker Compose.\n\nTo run the test containers you will need to have both Docker and Docker Compose installed on your system. To install the Docker engine on your system follow these [instructions](https://docs.docker.com/engine/install/). To verify your installation you can run the `hello-world` Docker image:\n```\ndocker run hello-world\n```\n\n#### Docker Compose\nDocker Compose is a separate binary which needs to be available on your system in order to run Yagna integration tests. `goth` requires `docker-compose` **version 1.27** or higher. There are two ways you can install it:\n1. Download the appropriate executable from the [releases page](https://github.com/docker/compose/releases) and make sure its present on your system\'s `PATH`.\n2. Use the `docker-compose` installed to your `goth` Python environment (you will need to activate the environment in the shell from which you run your tests).\n\n### Running the test network\n\n#### Getting a GitHub API token\nWhen first starting the test network, `goth` uses the GitHub API to fetch metadata and download artifacts and images. Although all of these assets are public, using the GitHub API still requires basic authentication. Therefore, you need to provide `goth` with a personal access token.\n\nTo generate a new token, go to your account\'s [developer settings](https://github.com/settings/tokens).\nYou will need to grant your new token the `public_repo` scope, as well as the `read:packages` scope. The packages scope is required in order to pull Docker images from GitHub.\n\nOnce your token is generated you need to do two things:\n1. Log in to GitHub\'s Docker registry by calling: `docker login docker.pkg.github.com -u {username}`, replacing `{username}` with your GitHub username and pasting in your access token as the password. You only need to do this once on your development machine.\n2. Export an environment variable named `GITHUB_API_TOKEN` and use the access token as its value. This environment variable will need to be available in the shell from which you run `goth`.\n\n### Running the integration tests\nWith project dependencies installed and environment set up you are now ready to launch integration tests.\n\nAll tests related to `yagna` can be found under `test/yagna` with end-to-end tests located in `test/yagna/e2e`. To run them, issue the below command from the project\'s root directory:\n```\npoetry run poe e2e_test\n```\nThe above command makes use of [`poethepoet`](https://github.com/nat-n/poethepoet), a task runner for `poetry`. To see all configured tasks run `poe` with no arguments:\n```\npoetry run poe\n```\n\nBy default, `poetry` looks for the required Python version on your `PATH` and creates a Python virtual environment for the project if there\'s none configured yet. All of the project\'s dependencies will be installed in that virtual environment.\n\nFor more granular control (e.g. running one specific test file) you can also invoke `pytest` directly to run tests:\n```\npytest -svx test/yagna/e2e/test_e2e_wasm.py\n```\n\nFollowing `pytest` convention, each test is defined as a separate Python function in a given `.py` file.\n\nEvery test run consists of the following steps:\n1. `docker-compose` is used to start the so-called "static" containers (e.g. local blockchain, HTTP proxy) and create a common Docker network for all containers participating in the test.\n2. The test runner creates a number of Yagna containers (as defined in the test\'s topology) which are connected to the `docker-compose` network.\n3. For each Yagna container started a so-called "probe" object is created and made available inside the test via the `Runner` object.\n4. The integration test scenario is executed as defined in the function called by `pytest`.\n5. Once the test is finished, all previously started Docker containers (both "static" and "dynamic") are removed.\n\n### Custom test options\n\n#### Assets path\nIt\'s possible to provide a custom assets directory which will be mounted in all Yagna containers used for the test. The assets include files such as the exe script definition (`exe-script.json`) or payment configuration (`accounts.json`).\n\nTo override the default path, use the `--assets-path` parameter, passing in the custom path:\n```\npoetry run poe e2e_test --assets-path test/custom_assets/some_directory\n```\n\n#### Log level\nBy default, the test runner will use `INFO` log level. To override it and enable more verbose logging, use the `--log-cli-level` parameter:\n```\npoetry run poe e2e_test --log-cli-level DEBUG\n```\n\n#### Logs path\nThe destination path for all test logs can be overridden using the option `--logs-path`:\n```\npoetry run poe e2e_test --logs-path your/custom/path\n```\n\n#### Yagna binary path\nBy default, a set of yagna binaries is downloaded from GitHub to be used for a given test session. The option `--yagna-binary-path` allows you to use binaries from the local file system instead. Its value must be a path to either a directory tree containing yagna binaries (e.g. `target` directory from a local `cargo` build) or a `.zip` archive file (e.g. downloaded manually from GitHub Actions):\n```\npoetry run poe e2e_test --yagna-binary-path /path/to/binaries\n```\n\n#### Yagna commit hash\nThis option makes `goth` use a `yagna` package associated with a specific git commit. The value here needs to be a git commit hash being the head for a successful GitHub Actions build workflow run:\n```\npoetry run poe e2e_test --yagna-commit-hash b0ac62f\n```\n\n#### Yagna .deb path\nPath to a local .deb file or a directory containing a number of such archives. All of these .deb files will be installed in the Docker image used for Yagna nodes in the tests. To specify the path, use the option `--yagna-deb-path`:\n```\npoetry run poe e2e_test --yagna-deb-path path/to/yagna.deb\n```\n\n#### Yagna release\nBy default, `goth` uses a `yagna` package from the latest GitHub release (or pre-release). To choose a different release to be used for a test run, use the option `--yagna-release`:\n```\npoetry run poe e2e_test --yagna-release 0.6.4-rc1\n```\nThe value for this option (`0.6.4-rc1` in the example above) should be a substring of the release\'s tag.\n\n### Troubleshooting integration test runs\nAll components launched during the integration test run record their logs in a pre-determined location. By default, this location is: `$TEMP_DIR/goth-tests`, where `$TEMP_DIR` is the path of the directory used for temporary files. This path will depend either on the shell environment or the operating system on which the tests are being run (see [`tempfile.gettempdir`](https://docs.python.org/3/library/tempfile.html) for more details). This default location can be overridden using the option `--logs-path` when running tests.\n\nThe logs from a test run are recorded in the following directory structure:\n- `runner.log` - logs recorded by the integration test runner engine.\n- `proxy.log` - logs recorded by the HTTP \'sniffer\' proxy, which monitors network traffic going into the yagna daemons launched for the test.\n-  `test_*` - directory with logs generated by nodes running as part of a single test (as defined in the test\'s topology). This directory is named after the name of the test scenario itself.\n The logs follow a straightforward naming convention, with daemons and their clients logging into dedicated files, eg.:\n   - `provider.log` - console output from `provider` yagna daemon.\n   - `provider_agent.log` - console output of the provider agent, running alongside `provider` daemon.\n',
    'author': 'Golem Factory',
    'author_email': 'contact@golem.network',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/golemfactory/goth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
