from odoo_somconnexio_python_client.client import Client


class DiscoveryChannel:
    _url_path = "/discovery-channel"

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def search(cls):
        """
        Return a list with all the discovery
        channels allowed in Odoo.

        :return: List of discovery channels
        """
        response_data = Client().get("{}".format(cls._url_path))

        discovery_channels = []
        for dc in response_data.get("discovery_channels"):
            discovery_channels.append(cls(**dc))

        return discovery_channels
