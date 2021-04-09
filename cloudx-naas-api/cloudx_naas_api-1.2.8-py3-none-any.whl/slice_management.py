"""
This module allows CloudX Edge Slice Management API set access
Following functions are exposed:
deploy_slice    allow easy to deploy slice on selected zones
undeploy_slice  allow easy to undeploy slice 

"""
import logging
import uuid

network = "cloudx-edge-us-8syz4"
user = "geneleblanc"
userFullname = "Gene LeBlanc"

logger = logging.getLogger()

def deploy_slice(profile, nw_location, tags=[]):
    """
    CloudX NaaS slide deployment function with following parameters:    
        profil         Name of slice profile e.g. lowlatency, 
                       highbandwidth. please use CloudX NaaS API to define profiles.
        nw_location    List of network locations for slice deployment 
        tags           Custom tags to be configured next to de slice deployment. 
                       The default tag:Name could be set for naming the deployed instance
    """
    message = f'Slice deployed on network {network} with {profile} for user {userFullname}'

    logger.info(message)
    
    return uuid.uuid4()


def undeploy_slice(id) :
    """
    CloudX NaaS slide undeployment function 
        id    Slice Id in UUID format to undeploy
    """

    return True

def main_f():
    deploy_slice(profile="hdvideo")


if __name__ == "__main__":
    main_f()
