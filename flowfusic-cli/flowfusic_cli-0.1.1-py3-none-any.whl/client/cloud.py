import src
from src.client.base import FlowfusicHttpClient
from src.exceptions import FlowfusicException
from src.log import logger


class CloudApiClient(FlowfusicHttpClient):
    """
    Client to interact with cloud api
    """

    def __init__(self, chunk_size=None, base_url=None):
        super(CloudApiClient, self).__init__()
        self.base_url = base_url or src.CLOUD_HTTPS_ENDPOINT

    def get_token(self):
        try:
            response = self.request("GET", "/api/get-token")
            data_dict = response.json()
            if not data_dict["token"]:
                logger.error("ERROR! Problem occured when tried to get token.")
                return None

            self.auth_header = "Bearer " + data_dict["token"]
            return data_dict["token"]
        except FlowfusicException as e:
            logger.info("ERROR! %s\n", e.message)
            return None

    def paraview_start(self):
        try:
            response = self.request("GET", "/api/paraview/start-server", timeout=120)
            data_dict = response.json()
            if not "started" in data_dict and not "ready" in data_dict:
                logger.error("ERROR! Problem occured when tried to start the server.")
                return None

            if "started" in data_dict and data_dict["started"]:
                return "started"
            if "ready" in data_dict:
                return "ready"

        except FlowfusicException as e:
            logger.info("ERROR! %s\n", e.message)
            return None

    def paraview_ready(self):
        try:
            response = self.request("GET", "/api/paraview/ready", timeout=10)
            data_dict = response.json()
            if not "ready" in data_dict:
                logger.error("ERROR! Problem occured when tried to start the server.")
                return None
            return data_dict["ready"]

        except FlowfusicException as e:
            logger.info("ERROR! %s\n", e.message)
            return None
