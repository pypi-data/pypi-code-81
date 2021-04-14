"""
A module that can interact with Cookie's API
"""

import requests

class Emotes:
  """
  To find Cookiemotes with ease.
  """
  def get_all(self):
    """
    Returns all of the Cookiemotes on CookieAPI
    """
    return requests.get("https://thatcookie-api.herokuapp.com/emotes").json()
  def get(self, name):
    """
    Searches for a Cookiemote by name.
    """
    return requests.get("https://thatcookie-api.herokuapp.com/emotes/" + name).json()
  def search(self, query):
    """
    Searches for a Cookiemote by name or by image url
    """
    return requests.get("https://thatcookie-api.herokuapp.com/emotes/search", query).json()

class Projects:
  def get_all(self):
    """
    Gets all of Cookie's Projects on his API.
    """
    return requests.get("https://thatcookie-api.herokuapp.com/projects").json()
  def get(self, number):
    """
    Gets one of Cookie's projects by its number.
    """
    return requests.get("https://thatcookie-api.herokuapp.com/projects/" + str(number)).json()
  def search(self, query):
    """
    Searches for a project by name, number, url or state.
    """
    return requests.get("https://thatcookie-api.herokuapp.com/projects/search", query).json()


class CCCprojects:
  def get_all(self):
    """
    Gets all of Cookie's Code Cups' projects on his API.
    """
    return requests.get("https://thatcookie-api.herokuapp.com/3C/projects").json()
  def get_by_3c_number(self, number):
    """
    Gets the projects of a Cookie's Code Cup its number.
    """
    return requests.get("https://thatcookie-api.herokuapp.com/3C/projects/" + str(number)).json()

class CCCparticipants:
  def get_all(self):
    """
    Gets all of Cookie's Code Cups' participants on his API.
    """
    return requests.get("https://thatcookie-api.herokuapp.com/3C/participants").json()
  def get_by_3c_number(self, number):
    """
    Gets the participant of a Cookie's Code Cup its number.
    """
    return requests.get("https://thatcookie-api.herokuapp.com/3C/participants/" + str(number)).json()

class CCC:
  def __init__(self):
    self.projects = CCCprojects()
    self.participants = CCCparticipants()
  def get_all(self):
    """
    Gets all of Cookie's Code Cups on his API.
    """
    return requests.get("https://thatcookie-api.herokuapp.com/3C").json()
  def get(self, number):
    """
    Gets one of Cookie's Code Cup by its number.
    """
    return requests.get("https://thatcookie-api.herokuapp.com/3C/" + str(number)).json()