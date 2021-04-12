"""
This module allows CloudX Edge GeoLocation and GeoFencing  Management API set 
Following functions are exposed:
create_geofence                      allow easy to define a geofence on selected zone
subscribe_to_geofence_notification   allow to subscribe to geofence breaches 

"""







class GeoLocation:
    def __init__(self, hosts=None, es=None):
        """
        Initialize an GEO Location API       
        """
        

    @classmethod
    def get_location(cls, es_url):
        "Get an GeoLocation from NaaS url"
        
        return ""


def create_geofence(geolocation,nw_locations):
    """
    API method to create geofence on selected nw_locations with following parameters:
    geolocation  GeoLocation Class to define the geofence location polygon
    nw_location    List of network locations for slice deployment 
    
    """

    return ""


def subscribe_to_geofence_notification(callback_function,geofence_id):
    """
    API method to subscribe to notifications for the breach on defined geofence
    callback_function   the callback function which should implement event sourcing
    geofence_id         the UUID of the geofence created
    """


    return ""
