"""
This module allows Cloud^X Edge IaaS Cluster Management API set
Following functions are exposed:

    deploy_application      allow easy to deploy application on selected locations
    undeploy_application    allow easy to destroy application 
    subscribe_to_service    allow to subscribe to service
    unsubscribe_to_service  allow to unsubscribe to service

"""


def deploy_application(cluster_ids, package_name, tags, **kwargs) -> str:
    """
    Cloud^X PaaS API function for cluster creation

    Parameters:    
        cluster_ids    Clusters for the applciation deployment
        nw_locations   List of network locations for slice deployment 
        tags           Custom tags to be configured next to de slice deployment. 
                       The default tag:Name could be set for naming the deployed instance
    Returns:
        application_id        The Application ID generated 
    """

    return ""


def undeploy_application(application_id, **kwargs) :
    """
    Cloud^X PaaS API function for undeploy application

    Parameters:    
        application_id    application Id for undeploy

    """

    return ""


def subscribe_to_service(nw_locations) -> str:
    """
    Cloud^X Edge PaaS API function to subscribe to service
    Enable the service for selected edge locations

    Parameters:        
        nw_locations       List of network locations for slice deployment         
    
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
