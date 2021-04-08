from mlploy import api_client
from mlploy import version


def print_version():
    api_version = api_client.version()
    print(f"MLPloy client v{version.__version__} and API v{api_version['version']}")
