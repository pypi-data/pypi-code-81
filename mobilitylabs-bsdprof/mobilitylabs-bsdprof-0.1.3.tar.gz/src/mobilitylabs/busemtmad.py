from mobilitylabs.core import MobilityLabs
import time
import logging
import requests

class BusEMTMad(MobilityLabs):
  '''Throughout this class you are able to leverage information about buses
     in the great city of Madrid, which is provided by the EMT (Empresa Municipal de Transportes)

     It extends the MobilityLabs class which encapsulates common functionality
     such authentication shared across several other classes.
  '''
  def __init__(self, x_client_id, pass_key):
    MobilityLabs.__init__(self, x_client_id, pass_key)

  def info_lines(self, date_ref):
    '''It returns the list of active lines in the reference date.

            Parameters:
                    date_ref (string): date reference in YYYYMMDD format

            Returns:
                    Array of JSON documents with information about the lines
                    or None if there was an error.
                    (See https://apidocs.emtmadrid.es/#api-Block_3_TRANSPORT_BUSEMTMAD-infolinegeneral for more info)
    '''
    url = "%s/transport/busemtmad/lines/info/%s/" % (self.MLURL, date_ref)
    headers = {'accessToken': self._access_token}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of lines retrieved: %s" % resp.json()['data'])
      return resp.json()['data']
      
    logging.error("Unable to retrieve the list of active lines with code '%s' and message: %s" %
                  (resp.status_code, resp.reason))
    return None

  def info_line(self, line_id, date_ref):
    '''It returns detailed info of a specific line in the reference date.

            Parameters:
                    line_id (string): bus line identifier
                    date_ref (string): date reference in YYYYMMDD format

            Returns:
                    Array of JSON documents (most likely with one single document) containing 
                    detailed information about the specified line or None if there was an error.
                    (See https://apidocs.emtmadrid.es/#api-Block_3_TRANSPORT_BUSEMTMAD-infolinedetail for more info)
    '''
    url = "%s/transport/busemtmad/lines/%s/info/%s/" % \
          (self.MLURL, line_id, date_ref)
    headers = {'accessToken': self._access_token}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of line '%s': %s" % \
                    (line_id, resp.json()['data']))
      return resp.json()['data']

    logging.error("Unable to retrieve the detailed info of line '%s'  with code '%s' and message: %s" %
                  (line_id, resp.status_code, resp.reason))
    return None

  def info_stops(self):
    '''It returns the list of active bus stops and information about them.

            Parameters:
                    None

            Returns:
                    Array of JSON documents, one per active bus stop, containing info about every
                    bus stop.
                    (See https://apidocs.emtmadrid.es/#api-Block_3_TRANSPORT_BUSEMTMAD-infostopgeneral for more info)
    '''
    url = "%s/transport/busemtmad/stops/list/" % self.MLURL
    headers = {'accessToken': self._access_token}
    resp = requests.post(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of active bus stops: %s" % resp.json()['data'])
      return resp.json()['data']

    logging.error("Unable to retrieve the list with active bus stops with code '%s' and message: %s" %
                  (resp.status_code, resp.reason))
    return None

  def info_stop(self, stop_id):
    '''It returns detailed info of a specific bus stop.

            Parameters:
                    stop_id (string): bus stop identifier

            Returns:
                    Array of JSON documents (most likely with one single document) containing
                    detailed information about the specified bus stop or None if there was an error.
                    (See https://apidocs.emtmadrid.es/#api-Block_3_TRANSPORT_BUSEMTMAD-detail_of_stop for more info)
    '''
    url = "%s/transport/busemtmad/stops/%s/detail/" % \
          (self.MLURL, stop_id)
    headers = {'accessToken': self._access_token}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of stop '%s': %s" % \
                    (stop_id, resp.json()['data']))
      return resp.json()['data']

    logging.error("Unable to retrieve the detailed info of stop '%s'  with code '%s' and message: %s" %
                  (line_id, resp.status_code, resp.reason))
    return None

  def line_stops(self, line_id,direction):
    '''It returns the list of stops of a line keeping in mind the direction

            Parameters:
                    line_id (string): bus line identifier
                    direction (string): "1" from start to end; "2" from end to start

            Returns:
                    Array of JSON documents (most likely with one single document) containing
                    info about the time table of the line plus every bus stop in the line.
                    (See https://apidocs.emtmadrid.es/#api-Block_3_TRANSPORT_BUSEMTMAD-stops for more info)
    '''
    url = "%s/transport/busemtmad/lines/%s/stops/%s/" % \
          (self.MLURL, line_id, direction)
    headers = {'accessToken': self._access_token}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of the stops of line '%s': %s" % \
                    (line_id, resp.json()['data']))
      return resp.json()['data']

    logging.error("Unable to retrieve the list of stops with code '%s' and message: %s" %
                  (resp.status_code, resp.reason))
    return None

  def issues(self, line_id):
    '''It returns details about incidents or issues identified and impacting bus lines.

            Parameters:
                    line_id (string): bus line identifier

            Returns:
                    Array of JSON documents (most likely with one single document) containing
                    info about incidents or issues identified and impacting bus lines.
                    (See https://apidocs.emtmadrid.es/#api-Block_3_TRANSPORT_BUSEMTMAD-incidents for more info)
    '''
    url = "%s/transport/busemtmad/lines/incidents/%s/" % \
          (self.MLURL, line_id)
    headers = {'accessToken': self._access_token}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Incidents or issues identified and impacting bus line '%s': %s" % \
                    (line_id, resp.json()['data']))
      return resp.json()['data']

    logging.error("Unable to retrieve the list of incidents for the bus line '%s' with code '%s' and message: %s" %
                  (line_id, resp.status_code, resp.reason))
    return None

  def buses_arrivals(self, stop_id, line_id=""):
    '''It returns the real time estimation of how far the buses are from the stop and how much time
       will take them to get to the bus stop. Only buses from the line specified will be considered.

            Parameters:
                    stop_id (string): bus stop identifier
                    line_id (string): bus line identifier. Optional parameter, if no provided all lines 
                                      for that stop will be considered.

            Returns:
                    Array of JSON documents (most likely with one single document) containing
                    info about arrival time, stop info, ...
                    (See https://apidocs.emtmadrid.es/#api-Block_3_TRANSPORT_BUSEMTMAD-arrives for more info)
    '''
    url = "%s/transport/busemtmad/stops/%s/arrives/%s/" % \
          (self.MLURL, stop_id, line_id)
    headers = {'accessToken': self._access_token}
    body = '{"cultureInfo":"EN", \
             "Text_StopRequired_YN":"Y", \
             "Text_EstimationsRequired_YN":"Y", \
             "Text_IncidencesRequired_YN":"N"}'
            
    resp = requests.post(url, headers=headers, data=body)

    if resp.status_code == 200:
      logging.debug("Buses arrival time and other info for stop '%s' in line '%s': %s" % \
                    (stop_id, line_id, resp.json()['data']))
      return resp.json()['data']

    logging.error("Unable to retrieve info of buses arrival time for the stop '%s' and bus line '%s' with code '%s' and message: %s" %
                  (stop_id, line_id, resp.status_code, resp.reason))
    return None
