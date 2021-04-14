from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from askoclics.askolib.client import Client

from future import standard_library

standard_library.install_aliases()


class DatasetClient(Client):
    """
    Manipulate datasets managed by Askomics
    """

    def list(self):
        """
        List datasets added in Askomics

        :rtype: list
        :return: List of datasets
        """

        return self._api_call("get", "list_datasets", {})['datasets']

    def delete(self, datasets):
        """
        Send a delete task on a list of datasets

        :type datasets: str
        :param datasets: Comma-separated list of datasets IDs

        :rtype: list
        :return: List of the datasets
        """

        datasets = self._parse_input_values(datasets, "Datasets")
        body = {'datasetsIdToDelete': datasets}

        return self._api_call("post", "delete_datasets", body)
