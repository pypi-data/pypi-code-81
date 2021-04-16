"""
This module allows Cloud^X Edge IaaS Cluster Management API set
Following functions are exposed:

    create_cluster          allow easy to create cluster on selected locations
    destroy_cluster         allow easy to destroy cluster 
    subscribe_to_service    allow to subscribe to service
    unsubscribe_to_service  allow to unsubscribe to service

"""

def create_cluster(autopilot,nw_locations, rbac, tags,**kwargs) -> str:
    """
    Cloud^X IaaS API function for cluster creation

    Parameters:    
        autopilot      Set the cluster autopilot, scale based on the loads
        nw_locations   List of network locations for slice deployment 
        tags           Custom tags to be configured next to de slice deployment. 
                       The default tag:Name could be set for naming the deployed instance
    Returns:
        cluster_id        The Slice ID generated 
    """
    

    return ""


def destroy_cluster(cluster_id, **kwargs) -> str:
    """
    Cloud^X IaaS API function for cluster destroy

    Parameters:    
        cluster_id    cluster Id for destroy

    """

    return ""

def subscribe_to_service(nw_locations) -> str:
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
