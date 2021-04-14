import requests
from requests.auth import HTTPBasicAuth
import json
from bs4 import BeautifulSoup
from ua_stache_api import ua_stache_api


import ua_eds_api


# Harvest EDS credentials from stache token.
with open("eds_stache_token.json", 'r') as file:
    contents = file.read()
stache_key, stache_url = ua_stache_api.get_entry(contents)
stache_secret = ua_stache_api.auth(stache_key, stache_url)
EDS_API = ua_eds_api.EdsApi(
    "https://eds-web.iam.arizona.edu/people",
    stache_secret["username"],
    stache_secret["password"],
    stache_secret["url"]
)


# Harvest Redmine credentials from stache token.
with open("redmine_creds_stache_token.json", 'r') as file:
    contents = file.read()
stache_key, stache_url = ua_stache_api.get_entry(contents)
stache_secret = ua_stache_api.auth(stache_key, stache_url)
REDMINE_URL = stache_secret["url"]
REDMINE_USERNAME = stache_secret["username"]
REDMINE_PASSWORD = stache_secret["password"]


def get_grouper_users():

    # Get all users in Grouper.
    grouper_users = EDS_API.get_grouper_users(
        "arizona.edu:dept:rii:redmine:ticketing")
    ids_admin = {member: False for member in members}

    # Get all admins in Grouper, append to dictionary.
    grouper_users = EDS_API.get_grouper_users(
        "arizona.edu:dept:rii:redmine:admins")
    ids_admin.update({member["id"]: True for member in members})

    grouper_users = dict()
    for member_id, admin in ids_admin.items():
        user = EDS_API.get_user(member_id)

        eds_username = user["uid"]
        ed_first_name, eds_last_name = user[
            "phoneBookDisplayName"].split(',')

        grouper_users[eds_username] = {"login": eds_username, "admin": admin}
        grouper_users[eds_username]["firstname"] = eds_first_name
        grouper_users[eds_username]["lastname"] = eds_last_name
        grouper_users[eds_username]["mail"] = user["mail"]

    return grouper_users


def get_redmine_users():
    """
    Gets all users in Redmine database.

    Returns:
        dict{str: dict} -> A dictionary of users, with user login as key, and
            dictionary of user attributes (including login) as value.
    """

    response = requests.get(
        f"{REDMINE_URL}/users.json",
        auth=HTTPBasicAuth(REDMINE_USERNAME, REDMINE_PASSWORD)
    )
    users = json.loads(response.content)["users"]
    return {user["login"]: user for user in users}


def synchronize(grouper, redmine):

    # Find all common keys.
    redmine_users = set(redmine)
    grouper_users = set(grouper)
    shared_users = grouper_users.intersection(redmine_users)
    new_redmine_users = grouper_users.difference(shared_users)
    redmine_users_to_delete = redmine_users.difference(shared_users)

    # Special case. This our api user, they live forever.
    redmine_users_to_delete.remove("rii-api-user")

    # Make sure all common users have the same admin status on both sites.
    for shared_user in shared_users:
        if redmine[shared_user]["admin"] != grouper[shared_user]["admin"]:
            redmine[shared_user]["admin"] = grouper[shared_user]["admin"]
            response = requests.put(
                f"{REDMINE_URL}/users/{redmine[shared_user]['id']}.json",
                auth=HTTPBasicAuth(REDMINE_USERNAME, REDMINE_PASSWORD),
                json={"user": redmine[shared_user]}
            )


    # Delete all redmine users not in grouper.
    for redmine_user in redmine_users_to_delete:
        response = requests.delete(
            f"{REDMINE_URL}/users/{redmine[redmine_user]['id']}.json",
            auth=HTTPBasicAuth(REDMINE_USERNAME, REDMINE_PASSWORD)
        )

    # Add all Grouper users not in redmine.
    headers = {'Content-type': 'application/json'}
    for new_user in new_redmine_users:
        response = requests.post(
            f"{REDMINE_URL}/users.json",
            auth=HTTPBasicAuth(REDMINE_USERNAME, REDMINE_PASSWORD),
            json={"user": grouper[new_user]},
        )


if __name__ == "__main__":
    grouper_users = get_grouper_users()
    redmine_users = get_redmine_users()
    synchronize(grouper_users, redmine_users)
