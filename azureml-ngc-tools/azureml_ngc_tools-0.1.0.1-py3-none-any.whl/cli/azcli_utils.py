import os
import sys
import json
import logging
import subprocess
from azure.cli.core import get_default_cli

logger = logging.getLogger("azureml_ngc.azutils")




def evaluate_az_cmd(az_cmd):
    print(az_cmd)
    cmd_proc = subprocess.run(az_cmd, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    # reading output and error
    cmd_stdout = cmd_proc.stdout.decode("utf-8")
    cmd_details = json.loads(cmd_stdout)
    return cmd_details

def az_cli(args_str):
    
    args = args_str.split()
    cli = get_default_cli()
    cli.invoke(args)
    if cli.result.result:
        return cli.result.result
    elif cli.result.error:
        raise cli.result.error
    return True

def get_resource_type_values(resource_type,search_args,value='name'):
    search_cmd = 'az {} list{}'.format(resource_type,search_args)
    cmd_details = evaluate_az_cmd(search_cmd)
    return [cmd_detail[value] for cmd_detail in cmd_details]

def resource_exist(resource_type,resource_name,search_args):
    print("Searching for {}; Named: {}".format(resource_type,resource_name))
    return resource_name in get_resource_type_values(resource_type,search_args)

def get_resources_args(resource_group):
    priority = 500

    if resource_exist('network nsg','{0}-nsg'.format(resource_group),''):
        priorities = get_resource_type_values('network nsg rule',' --nsg-name {0}-nsg -g {0}'.format(resource_group),'priority')
        if priority in priorities:
           priority = max(priorities)+1 

    resources_args = {'vnet':{},'nsg':{},'nsg rule':{}}
    resources_args['vnet']['s']=''
    resources_args['nsg']['s']=''
    resources_args['nsg rule']['s']=' --nsg-name {0}-nsg -g {0}'.format(resource_group)
    resources_args['vnet']['c']=' --address-prefix 10.0.0.0/16 --subnet-name default --subnet-prefix 10.0.0.0/24'
    resources_args['nsg']['c']=''
    resources_args['nsg rule']['c'] = (
        ' --nsg-name {}-nsg --priority {} --source-address-prefixes Internet'
        ' --destination-port-ranges 8786 8787 8888 --destination-address-prefixes "*"'
        ' --access Allow --protocol Tcp  --description "Allow Internet to Dask on ports 8786 8787 8888."'
    ).format(resource_group, priority)
    return resources_args

def set_resource(resource_group,resource_type,resource_name,search_args,create_args):
    if resource_exist(resource_type,resource_name,search_args):
        print('{} was found\n'.format(resource_name))
    else:
        print('Creating {}\n'.format(resource_name))
        evaluate_az_cmd('az {} create -g {} -n {}{}'.format(resource_type,resource_group,resource_name,create_args))

def set_resources(resource_group,location):
    resources_args = get_resources_args(resource_group)
    for resource_type, args in resources_args.items():
        set_resource(resource_group,'network {}'.format(resource_type),
        '{}-{}'.format(resource_group,"_".join(resource_type.split())),args['s'],args['c'])
    return ['{}-{}'.format(resource_group,"_".join(x.split())) for x in resources_args.keys()]

def login():
    az_cli("login")
    return
