# -*- coding: utf-8 -*-
"""Okta class file for Gaia."""
import requests


class Okta:
    """Okta class."""

    def __init__(self, token, verbose=False):
        """Initialize a Gaia class instance."""
        self.base_url = "https://broadinstitute.okta.com/api/v1"
        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": f"SSWS {token}",
        }
        self.verbose = verbose

    #
    # App Users
    #
    def add_app_user(self, app_id, body):
        """Add a user to an application."""
        url = f"{self.base_url}/apps/{app_id}/users"
        return requests.post(url, json=body, headers=self.headers)

    def get_app_users(self, app_id):
        """Return a list of users assigned to an application."""
        url = f"{self.base_url}/apps/{app_id}/users"
        users = []
        while url:
            response = requests.get(url, headers=self.headers)
            url = response.links.get("next", {}).get("url")
            users.extend(response.json())
        return users

    def get_apps(self):
        """Return a list of apps."""
        url = f"{self.base_url}/apps"
        apps = []
        while url:
            response = requests.get(url, headers=self.headers)
            url = response.links.get("next", {}).get("url")
            apps.extend(response.json())
        return apps

    #
    # User Types
    #
    def get_user_types(self):
        """Return a list of all uesr types."""
        url = f"{self.base_url}/meta/types/user"
        usertypes = []
        while url:
            response = requests.get(url, headers=self.headers)
            url = response.links.get("next", {}).get("url")
            usertypes.extend(response.json())
        return usertypes

    def get_user_types_by_name(self):
        """Return a dict of user types by name."""
        usertypes = {}
        for t in self.get_user_types():
            name = t["name"]
            usertypes[name] = t
        return usertypes

    #
    # Users
    #
    def create_user(self, body, activate=False):
        """Create a new Okta user."""
        url = f"{self.base_url}/users"
        params = {
            "activate": activate,
            "provider": True,
        }
        return requests.post(url, headers=self.headers, json=body, params=params)

    def get_users(self):
        """Return a list of users."""
        url = f"{self.base_url}/users"
        users = []
        while url:
            response = requests.get(url, headers=self.headers)
            url = response.links.get("next", {}).get("url")
            users.extend(response.json())
        return users

    def get_users_by_email(self):
        """Return a dict of users by email address."""
        users = {}
        for u in self.get_users():
            email = u["profile"]["email"]
            users[email] = u
        return users

    def update_user(self, user_id, user):
        """Update a single Okta user by ID."""
        url = f"{self.base_url}/users/{user_id}"
        return requests.put(url, headers=self.headers, json=user)
