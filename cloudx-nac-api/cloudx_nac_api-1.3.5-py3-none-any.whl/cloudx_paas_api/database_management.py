"""
This module allows Cloud^X Edge PaaS Database Management API set
Following functions are exposed:

    create_database         allow easy to create database service
    destroy_database        allow easy to delete database service   
    subscribe_to_service    allow to subscribe to service
    unsubscribe_to_service  allow to unsubscribe to service

"""


def create_database(nw_locations, type="MariaDB",profile="Default_iops",**kwargs) -> str:
    """
    Cloud^X Edge PaaS API function to create database instance 
    Enable the service for selected edge locations

    Parameters:        
        nw_locations       List of network locations for slice deployment   
        type               Following database types are provided:
                           MariaDB
                           PostgresSQL
                           MongoDB
                           Apache Casandra
                           Apache Aerospike
        profile            profile selection for IOPS

    
    Returns:
        database_id        The Database ID generated 
    """


    return "database_id"


def destroy_database(database_id, **kwargs) -> str:
    """
    Cloud^X PaaS API function for database destroy 

    Parameters:    
        database_id     Database ID for destroy
    """

    return ""

def subscribe_to_service(nw_locations, retention, **kwargs) -> str:
    """
    Cloud^X Edge PaaS API function to subscribe to service
    Enable the service for selected edge locations

    Parameters:        
        nw_locations       List of network locations for slice deployment   
        retention          Retention period to keep monitoring metrics 
    
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
