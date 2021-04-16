"""
This module allows Cloud^X Edge IaaS Load Balancer Management API set
Following functions are exposed:

    create_load_balancer    allow easy to create load balancer 
    destroy_load_balancer    allow easy to delete load balancer 
    create_target           allow easy to create target
    subscribe_to_service    allow to subscribe to service
    unsubscribe_to_service  allow to unsubscribe to service

"""


def create_load_balancer(nw_locations, type="Application", profile="Default", security_profile="Default", **kwargs) -> str:
    """
    Cloud^X Edge IaaS API function to create database instance 
    Enable the service for selected edge locations

    Parameters:        
        nw_locations       List of network locations for load balancer  
        type               Following load balancer types are provided:
                           Application LB
                           Network LB
        profile            profile selection for load balancer
        security_profile   security profile selection, default is "Default" profile 
                           allows 80 and 443 ports

    
    Returns:
        load_balancer_id        The Load Balancer instance ID generated 
    """

    return ""


def destroy_load_balancer(load_balancer_id, **kwargs):
    """
    Cloud^X IaaS API function for load balancer destroy 

    Parameters:    
        load_balancer_id     Laod Balancer ID for destroy
    """

    return ""


def create_target(nw_locations, load_balancer_id, application_list, ** kwargs) -> str:
    """
    Cloud^X Edge IaaS API function to create database instance 
    Enable the service for selected edge locations

    Parameters:        
        nw_locations       List of network locations for target app
        load_balancer_id   Load Balancer id to attach the target
        application_list   List of application profile to enable for target 

    
    Returns:
        target_id        The Target ID generated 
    """

    return ""


def subscribe_to_service(nw_locations, retention, **kwargs) -> str:
    """
    Cloud^X Edge IaaS API function to subscribe to service
    Enable the service for selected edge locations

    Parameters:        
        nw_locations       List of network locations for slice deployment           
    
    Returns:
        service_id        The Service ID generated 
    """

    return True


def unsubscribe_to_service(service_id):
    """
    Cloud^X Edge IaaS API function to unsubscribe to service
    Disable the service for selected edge locations
    
    Parameters:
        service_id        Service Id to disable
    """

    return True
