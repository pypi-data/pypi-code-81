from mobilitylabs.core import MobilityLabs
import logging
import requests

class BiciMad(MobilityLabs):
  '''Throughout this class you are able to leverage information about bikes and bike stations
     in the great city of Madrid, which is provided by the BiciMAD GO service.

     It extends the MobilityLabs class which encapsulates common functionality
     such authentication shared across several other classes.
  '''
  def __init__(self, x_client_id, pass_key):
    MobilityLabs.__init__(self, x_client_id, pass_key)

  def info_bike_stations(self):
    '''It returns the details of Madrid BiciMad Stations.

            Parameters:
                    None

            Returns:
                    Array of JSON documents with information about the bike stations
                    or None if there was an error.
                    (See https://apidocs.emtmadrid.es/#api-Block_4_TRANSPORT_BICIMAD-List_of_Bicimad_Stations for more info)
    '''
    url = "%s/transport/bicimad/stations/" % self.MLURL
    headers = {'accessToken': self._access_token}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of bike stations retrieved: %s" % resp.json()['data'])
      return resp.json()['data']

    logging.error("Unable to retrieve the list of bike stations with code '%s' and message: %s" %
                  (resp.status_code, resp.reason))
    return None

  def info_bike_station(self, bike_station_id):
    '''It returns the details of a specific Madrid BiciMad Station.

            Parameters:
                    bike_station_id (string): bike station identifier

            Returns:
                    Array of JSON documents (most likely with one single document) with information 
                    about the bike stations or None if there was an error.
                    (See https://apidocs.emtmadrid.es/#api-Block_4_TRANSPORT_BICIMAD-List_of_Bicimad_Stations for more info)
    '''
    url = "%s/transport/bicimad/stations/%s" % (self.MLURL, bike_station_id)
    headers = {'accessToken': self._access_token}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of bike station '%s': %s" % (bike_station_id, resp.json()['data']))
      return resp.json()['data']

    logging.error("Unable to retrieve info for bike station '%s' with code '%s' and message: %s" %
                  (bike_station_id, resp.status_code, resp.reason))
    return None

  def info_bikes(self):
    '''It returns the details of Madrid BiciMad bikes.

            Parameters:
                    None

            Returns:
                    Array of JSON documents with information about the bikes available in the
                    BiciMad service or None if there was an error.
                    (See https://apidocs.emtmadrid.es/#api-Block_4_TRANSPORT_BICIMAD-List_of_BiciMAD_GO_bikes_on_realtime for more info)
    '''
    url = "%s/transport/bicimadgo/bikes/availability/" % self.MLURL
    headers = {'accessToken': self._access_token}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of bikes in the service: %s" % resp.json()['data'])
      return resp.json()['data']

    logging.error("Unable to retrieve the info of the bikes with code '%s' and message: %s" %
                  (resp.status_code, resp.reason))
    return None

  def info_bike(self, bike_id):
    '''It returns the details of a specific bike from the Madrid BiciMad service.

            Parameters:
                    bike_id (string): bike identifier

            Returns:
                    Array of JSON documents with information about a specific bike from the
                    BiciMad service or None if there was an error.
                    (See https://apidocs.emtmadrid.es/#api-Block_4_TRANSPORT_BICIMAD-List_of_BiciMAD_GO_bikes_on_realtime for more info)
    '''
    url = "%s/transport/bicimadgo/bikes/availability/%s" % (self.MLURL, bike_id)
    headers = {'accessToken': self._access_token}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of bike '%s' in the service: %s" % (resp.json()['data'], bike_id))
      return resp.json()['data']

    logging.error("Unable to retrieve the info of bike '%s' with code '%s' and message: %s" %
                  (bike_id, resp.status_code, resp.reason))
    return None

