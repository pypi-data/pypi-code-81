import time
import logging
import requests

class MobilityLabs:

  MLURL = "https://openapi.emtmadrid.es/v1"
  _x_client_id = ""
  _pass_key = ""
  _access_token = ""
  _token_sec_expiration = 0
  _logged_in = False

  def __init__(self, x_client_id, pass_key):
    logging.basicConfig(level=logging.DEBUG)
    self._x_client_id = x_client_id
    self._pass_key = pass_key
    logging.debug("New MobilityLabs instance for X-ClientId '%s'" % self._x_client_id)

  def is_logged_in(self):
    return self._logged_in

  def log_in(self):
    url = "%s/mobilitylabs/user/login/" % self.MLURL
    headers = {'X-ClientId': self._x_client_id, 'passKey': self._pass_key}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      response = resp.json()
      self._access_token = response['data'][0]['accessToken']
      self._token_sec_expiration = time.time() + response['data'][0]['tokenSecExpiration']
      self._logged_in = True
      logging.debug("Token '%s' created and will expire %d seconds" %
                    (self._access_token, response['data'][0]['tokenSecExpiration']))
      return True

    logging.error("Unable to log in with code '%s' and message: %s" % 
                  (resp.status_code, resp.reason))
    return False
