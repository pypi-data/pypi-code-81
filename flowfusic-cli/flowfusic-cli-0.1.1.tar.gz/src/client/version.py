import src
from src.client.base import FlowfusicHttpClient
from src.log import logger
from src.model.version import CliVersion


class VersionClient(FlowfusicHttpClient):
    """
    Client to get API version from the server
    """

    def __init__(self):
        super(VersionClient, self).__init__(skip_auth=True)
        self.url = "/api/v1/cli_version"
        self.base_url = src.CLOUD_HTTPS_ENDPOINT

    def get_cli_version(self):
        response = self.request("GET", self.url)
        data_dict = response.json()
        logger.debug("CLI Version info: %s", data_dict)
        return CliVersion.from_dict(data_dict)
