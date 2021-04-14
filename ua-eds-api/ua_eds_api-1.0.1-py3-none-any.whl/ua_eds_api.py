import requests
from requests.auth import HTTPBasicAuth
import json
from bs4 import BeautifulSoup


class EdsApi():
    def __init__(self, host, username, password, grouper):
        self.host = host
        self.username = username
        self.password = password
        self.grouper = grouper

    def get_user(self, identifier):
        """
        Harvest all eds information for a given user.

        Parameters:
            identifier (str): Must be either a username or and id in EDS
                registry.
        Returns:
            user (dict): A dictionary of all data values for the given
                requested user.
        """
        # Grab eds response as soup.
        response = requests.get(
            f"{self.host}/{identifier}",
            auth=HTTPBasicAuth(self.username, self.password)
        )
        response.raise_for_status()
        eds_soup = BeautifulSoup(response.content, "xml")

        user = dict()
        for attribute in eds_soup.find_all("dsml:attr"):
            # Grab all values for the attribute. If only one value, convert to
            # not be list.
            values = list()
            for value in attribute.find_all("dsml:value"):
                values.append(value.text.strip())
            if len(values) == 1:
                values = values[0]
            user[attribute["name"]] = values
        return user

    def get_grouper_users(self, group):
        """
        Harvest all the members of a grouper group.

        Parameters:
            group (str): Name of group to harvest from.
        Returns:
            (dict): Mapping of id to a dictionary of data for each user in
                group.
        """
        response = requests.get(
            f"{self.grouper}/{group}/members",
            auth=HTTPBasicAuth(self.username, self.password)
        )
        response.raise_for_status()

        members = json.loads(
            response.content)["WsGetMembersLiteResult"]["wsSubjects"]
        return {member["id"]: member for member in members}
