from mobilitylabs.core import MobilityLabs
import logging
import requests

class ParkingEMTMad(MobilityLabs):
  '''Throughout this class you are able to leverage information about parking areas
     in the great city of Madrid, which is provided by the EMT (Empresa Municipal de Transportes)

     It extends the MobilityLabs class which encapsulates common functionality
     such authentication shared across several other classes.
  '''
  def __init__(self, x_client_id, pass_key):
    MobilityLabs.__init__(self, x_client_id, pass_key)

  def info_parkings(self):
    '''It returns the list of active parking areas operated by the EMT.

            Parameters:
                    None

            Returns:
                    Array of JSON documents with information about the parking areas
                    or None if there was an error.
                    (See https://apidocs.emtmadrid.es/#api-Block_5_PARKINGS-parking_list for more info)
    '''
    url = "%s/citymad/places/parkings/EN/" % self.MLURL
    headers = {'accessToken': self._access_token}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of parking areas retrieved: %s" % resp.json()['data'])
      return resp.json()['data']

    logging.error("Unable to retrieve the list parking areas with code '%s' and message: %s" %
                  (resp.status_code, resp.reason))
    return None

  def info_parking(self, parking_id):
    '''It returns the details of a specific parking area.

            Parameters:
                    parking_id (string): parking area identifier

            Returns:
                    Array of JSON documents (most likely with one single document) with information
                    about the parking area or None if there was an error.
                    (See https://apidocs.emtmadrid.es/#api-Block_5_PARKINGS-parking_detail for more info)
    '''
    url = "%s/citymad/places/parking/%s/EN/" % (self.MLURL,parking_id)
    headers = {'accessToken': self._access_token}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of parking area '%s': %s" % (parking_id, resp.json()['data']))
      return resp.json()['data']

    logging.error("Unable to retrieve info for parking area station '%s' with code '%s' and message: %s" %
                  (parking_id, resp.status_code, resp.reason))
    return None

  def availability(self):
    '''It returns availability for those parking areas publishing this information. Not all
       of them make this information public.

            Parameters:
                    None

            Returns:
                    Array of JSON documents (most likely with one single document) with information
                    about the availabitily of parking areas or None if there was an error.
                    (See https://apidocs.emtmadrid.es/#api-Block_5_PARKINGS-parking_availability for more info)
    '''
    url = "%s/citymad/places/parkings/availability/" % (self.MLURL)
    headers = {'accessToken': self._access_token}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of the availability of parking areas: %s" % resp.json()['data'])
      return resp.json()['data']

    logging.error("Unable to retrieve availability of parking areas with code '%s' and message: %s" %
                  (resp.status_code, resp.reason))
    return None
