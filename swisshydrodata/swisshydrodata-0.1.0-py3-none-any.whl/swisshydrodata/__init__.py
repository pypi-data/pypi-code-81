import requests
import logging

logger = logging.getLogger(__name__)

class SwissHydroData:
    """
    SwissHydroData enables you to fetch data from
    the Federal Office for the Environment FOEN
    """

    def __init__(self):
        self.base_url = "https://swisshydroapi.bouni.de/api/v1"

    def get_stations(self):
        """ Return a list of all stations IDs """
        request = requests.get("{}/stations".format(self.base_url))
        if request.status_code != 200:
            logger.error(f"Request for list of stations failed with status code {request.status_code}")
            return None
        return request.json()

    def get_station(self, station_id):
        """ Return all data for a given station """
        request = requests.get("{}/station/{}".format(self.base_url, station_id))
        if request.status_code != 200:
            logger.error(f"Request for station {station_id} failed with status code {request.status_code}")
            return None
        return request.json()
