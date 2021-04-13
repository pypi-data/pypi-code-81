#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import os
from colorama import Fore, Style
from aos_signer.signer.errors import NoAccessError

_meta_folder_name = 'meta'
_src_folder_name = 'src'
_config_file_name = 'config.yaml'


def run_bootstrap():
    _create_folder_if_not_exist(_meta_folder_name)
    _create_folder_if_not_exist(_src_folder_name)
    _init_conf_file()
    print(Fore.GREEN + "DONE" + Style.RESET_ALL + '\n')
    _print_epilog()


def _create_folder_if_not_exist(folder_name):
    try:
        if os.path.isdir(folder_name):
            print("Directory {}[{}]{} exists... {}Skipping{}".format(
                Fore.CYAN, folder_name, Style.RESET_ALL, Fore.YELLOW, Style.RESET_ALL)
            )
        else:
            os.mkdir(folder_name)
            print("Directory {}[{}]{} created.".format(Fore.CYAN, folder_name, Style.RESET_ALL))
    except PermissionError:
        raise NoAccessError


def _init_conf_file():
    conf_file_path = os.path.join(_meta_folder_name, _config_file_name)
    if os.path.isfile(conf_file_path):
        print("Configuration file {cyan}[{filename}]{reset} exists... {yellow}Skipping{reset}".format(
            cyan=Fore.CYAN, filename=_config_file_name, reset=Style.RESET_ALL, yellow=Fore.YELLOW)
        )
    else:
        with open(conf_file_path, 'x') as cfp:
            cfp.write(_config_bootstrap)
        print("Config file {}/{} created".format(_meta_folder_name, _config_file_name))


def _print_epilog():
    print('---------------------------')
    print(Style.DIM + 'Further steps:')
    print("Copy your service files with desired folders to 'src' folder.")
    print("[optional] Copy your private key (" + Fore.CYAN + "private_key.pem" + Fore.RESET + Style.DIM +
          ") and Service Provider certificate (" + Fore.CYAN + "sp-client.pem" + Fore.RESET + ") to meta folder.")
    print("Update " + Fore.CYAN + "meta/config.yaml" + Fore.RESET + " with desired values.")
    print("Run '" + Style.BRIGHT + Fore.BLUE + "aos-signer sign" + Style.RESET_ALL + Style.DIM +
          "' to sign service and '" + Style.BRIGHT + Fore.BLUE + "aos-signer upload" + Style.RESET_ALL + Style.DIM +
          "' to upload signed service to the cloud.")


_config_bootstrap = """
# Commented sections are optional. Uncomment them if you want to include them in config

#publisher: # General publisher info section
#    author: # Author info
#    company: # Company info

# How to build and sign package
build:
    os: linux
    arch: x86
    sign_key: private_key.pem
    sign_certificate: sp-client.pem
    symlinks: copy
    # context: string, optional

# Information about publishing process (URI, cert, etc)
publish:
    url: aoscloud.io
    service_uid: #Service UID Can be found on Service page 
    tls_key: private_key.pem
    tls_certificate: sp-client.pem

# Service configuration
configuration:
    state:
        filename: state.dat
        required: False

    # Startup command
    cmd: string
    # Service working dir
    workingDir: string

#    devices:
#        - name : string (camera0, mic0, audio0, etc)
#          mode  : rwm

#    resources:
#        - system-dbus
#        - bluetooth
        
#    hostname: my-container
    
#    exposedPorts:
#        - 8089-8090/tcp
#        - 1515/udp
#        - 9000

#    allowedConnections:
#        - 9931560c-be75-4f60-9abf-08297d905332/8087-8088/tcp
#        - 9931560c-be75-4f60-9abf-08297d905332/1515/udp

#    Quotas assigned to service
#      quotas:
#        cpu: 50
#        mem: 2KB
#        state: 64KB
#        storage: 64KB
#        upload_speed: 32Kb
#        download_speed: 32Kb
#        upload: 1GB
#        download: 1GB
#        temp: 32KB
#   
#  Resource alerts
#    alerts:
#        ram:
#            minTime: string
#            minThreshold: 10,
#            maxThreshold: 150
#        cpu:
#            minTime: string
#            minThreshold: 40,
#            maxThreshold: 45
#        storage:
#            minTime: string
#            minThreshold: 10,
#            maxThreshold: 150
#        upload:
#            minTime: string
#            minThreshold: 10,
#            maxThreshold: 150
#        download:
#            minTime: string
#            minThreshold: 10,
#            maxThreshold: 150
#
#    Permissions for functional servers
#    permissions:
         # functional server
#        vis:
             # functionality name: access mode
#            Attribute.Body.Vehicle.VIN: "r"
#            Signal.Doors.* : "rw"
"""
