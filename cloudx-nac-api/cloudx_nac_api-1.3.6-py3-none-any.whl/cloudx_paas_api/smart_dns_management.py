"""
This module allows Cloud^X Edge PaaS Smart DNS Management API set
Following functions are exposed:

    subscribe_to_service    allow to subscribe to service
    unsubscribe_to_service  allow to unsubscribe to service

"""


def subscribe_to_service(nw_locations, failover_zones = [], **kwargs) -> str:
    """
    Cloud^X Edge PaaS API function to subscribe to service
    Enable the service for selected edge locations

    Parameters:        
        nw_locations       List of network locations for slice deployment   
        failover_zone      The zone name fro failover of DNS queries
    
    Returns:
        service_id        The Service ID generated 
    """

    return True


def unsubscribe_to_service(service_id):
    """
    Cloud^X Edge PaaS API function to unsubscribe to service
    Disable the service for selected edge locations
    
    Parameters:
        service_id        Service Id to disable
    """

    return True
