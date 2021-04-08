import logging

from azureml.core import Workspace, Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.compute import ComputeTarget, AmlCompute
import click, os, time, re
from azureml_ngc_tools.AzureMLComputeCluster import AzureMLComputeCluster
from azureml_ngc_tools.cli import ngccontent
from azureml_ngc_tools.cli import azcli_utils
from azureml.exceptions._azureml_exception import ProjectSystemException
from dask_cloudprovider.azure import AzureVMCluster
from dask.distributed import Client

### SETUP LOGGING
fileFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.10s]  %(message)s")
logger = logging.getLogger("azureml_ngc")
logger.setLevel("DEBUG")

fileHandler = logging.FileHandler("azureml_ngc_tools.log", mode="w")
fileHandler.setFormatter(fileFormatter)
logger.addHandler(fileHandler)

def log(message,local=True):
    logger.info(message)
    if (local):
        print(message)

@click.command()
@click.option(
    "--login", is_flag=False, required=True, help="Path to the login config file"
)
@click.option("--app", is_flag=False, required=True, help="Path to the config file")
@click.version_option()
def start(login, app):
    install_packages()
    login_config = ngccontent.get_config(login)
    app_config = ngccontent.get_config(app)
    ### WORKSPACE
    ws = getWorkspace(login_config,logger)

    ### GPU RUN INFO
    gpus_per_node = validateVMSize(ws,login_config,logger)

    useDask = figureDaskUsage(login_config)
    
    if (not useDask):
        ct, pri_key_file = setUpComputeTarget(ws,login_config)
        env = createOrGetEnvironment(ws, login_config, app_config)
        cluster, jupyter_link = getAzureMLComputeCluster(ws,ct,env,login_config,pri_key_file)
    else:
        azcli_utils.login()
        log("\nCreating a Dask Cluster with {} nodes".format(login_config["aml_compute"]["max_nodes"]))
        cluster, jupyter_link, client = getAzureVMCluster(ws,gpus_per_node,login_config,app_config)
        

    ### UPLOAD ADDITIONAL CONTENT IF NOT EXISTS
    for additional_content in app_config["additional_content"]["list"]:
        url = additional_content["url"]
        targetfile = additional_content["filename"]
        src_path = additional_content["localdirectory"]
        dest_path = additional_content["computedirectory"]

        if (useDask):
            load_content_to_scheduler(url,targetfile,src_path,dest_path,additional_content,app_config,client)
        else:
            load_content(url,targetfile,src_path,dest_path,additional_content,app_config,ws)
    
    if (useDask):
        client.close()
    
    log(f"\n    Go to: {jupyter_link}")
    log("    Press Ctrl+C to stop the cluster.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        log("\nClosing Cluster ...")
        cluster.close()

def install_packages():
    import subprocess
    import sys
    packages = ["azure.cli.core"]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def figureDaskUsage(login_config):
    useDask = False
    if (
        login_config["aml_compute"]["max_nodes"]>1 
        or (login_config["aml_compute"]["max_nodes"]==1
        and 'dask' in login_config["aml_compute"]
        and login_config["aml_compute"]['dask']==True)
        ):
        useDask = True
    return useDask


def validateVMSize(ws,login_config,logger):
    vm_name = login_config["aml_compute"]["vm_name"].lower()
    workspace_vm_sizes = AmlCompute.supported_vmsizes(ws)
    pascal_volta_pattern = pattern = re.compile(
        r"[a-z]+_nc[0-9]+[s]?_v[2,3]"
    )  ### matches NC-series v2 and v3
    workspace_vm_sizes = [
        (e["name"].lower(), e["gpus"])
        for e in workspace_vm_sizes
        if pattern.match(e["name"].lower())
    ]
    workspace_vm_sizes = dict(workspace_vm_sizes)
    gpus_per_node = -1
    ### GET NUMBER OF GPUS PER VM
    if vm_name in workspace_vm_sizes:
        gpus_per_node = workspace_vm_sizes[vm_name]
        log("\n    VM SIze {} was recognized\n".format(vm_name))
    else:
        logger.exception("Unsupported vm_size {vm_size}".format(vm_size=vm_name))
        logger.exception("The specified vm size must be one of ...")

        for azure_gpu_vm_size in workspace_vm_sizes.keys():
            logger.exception("... " + azure_gpu_vm_size)
        raise Exception(
            "{vm_size} does not have Pascal or above GPU Family".format(vm_size=vm_name)
        )

    verify = f"""
    Number of GPUs per node: {gpus_per_node}
    """
    log(verify)

    return gpus_per_node

def getWorkspace(login_config,logger):
    subscription_id = login_config["azureml_user"]["subscription_id"]
    resource_group = login_config["azureml_user"]["resource_group"]
    workspace_name = login_config["azureml_user"]["workspace_name"]

    try:
        ws = Workspace(
            workspace_name=workspace_name,
            subscription_id=subscription_id,
            resource_group=resource_group,
        )
    except ProjectSystemException:
        msg = f'\n\nThe workspace "{workspace_name}" does not exist. '
        msg += f"Go to \n\n  "
        msg += f"-->> https://docs.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace <<--\n\n"
        msg += f"and create the workspace first.\n\n\n"
        msg += f"Your current configuration: \n\n"
        msg += f"Workspace name: {workspace_name} \n"
        msg += f"Subscription id: {subscription_id} \n"
        msg += f"Resource group: {resource_group}\n\n"
        logger.exception(msg)
        raise Exception(msg)

    verify = f"""
    Subscription ID: {subscription_id}
    Resource Group: {resource_group}
    Workspace: {workspace_name}"""
    log(verify)

    return ws

def getAzureVMCluster(ws,gpus_per_node,login_config,app_config):
    location = ws.location
    resource_group = login_config["azureml_user"]["resource_group"]
    resources = azcli_utils.set_resources(resource_group,location)
    vnet = resources[0]
    security_group = resources[1]
    EXTRA_PIP_PACKAGES = login_config["aml_compute"]["pip_packages"]
    n_workers=int(login_config["aml_compute"]["max_nodes"])

    verify = f"""
    docker_image: {app_config["base_dockerfile"]}
    vm_size: {login_config["aml_compute"]["vm_name"]}
    resource_group: {resource_group}
    vnet: {vnet}
    security_group: {security_group}
    location: {location}"""
    log(verify)

    log(AzureVMCluster.get_cloud_init(
        resource_group=resource_group,
        location = location,
        vnet=vnet,
        security_group=security_group,
        n_workers=n_workers,
        vm_size=login_config["aml_compute"]["vm_name"],
        docker_image=app_config["base_dockerfile"],
        docker_args="--privileged",
        auto_shutdown=False,
        security=False,
        env_vars={"EXTRA_PIP_PACKAGES": EXTRA_PIP_PACKAGES},
        worker_class="dask_cuda.CUDAWorker"))
    
    cluster = AzureVMCluster(
        resource_group=resource_group,
        location = location,
        vnet=vnet,
        security_group=security_group,
        n_workers=n_workers,
        vm_size=login_config["aml_compute"]["vm_name"],
        docker_image=app_config["base_dockerfile"],
        docker_args="--privileged",
        auto_shutdown=False,
        security=False,
        env_vars={"EXTRA_PIP_PACKAGES": EXTRA_PIP_PACKAGES},
        worker_class="dask_cuda.CUDAWorker")
        
    log("All {} workers have been created\n".format(n_workers))

    client = Client(cluster)
    num_expected_total_gpus = n_workers*gpus_per_node

    log("Setting {} workers on the cluster for a total of {} GPUs\n".format(n_workers,num_expected_total_gpus))
    cluster.scale(n_workers)
    client = Client(cluster)
    
    num_provisioned_gpus = -1
    
    while (not len(client.nthreads().keys()) == num_expected_total_gpus):
        if(len(client.nthreads().keys())==num_provisioned_gpus):
            print(".", end="")
            time.sleep(5)
        else:
            num_provisioned_gpus = len(client.nthreads().keys())
            print("\nNumber of GPUs added to the cluster {} out of {}".format(num_provisioned_gpus,num_expected_total_gpus))
    print("\nNumber of GPUs added to the cluster {} out of {}".format(len(client.nthreads().keys()),num_expected_total_gpus))
    print('All requested {} GPUs have been added to the cluster'.format(num_expected_total_gpus))
    
    jupyter_link = "{}:8888".format(cluster.scheduler_address.split(':')[1].split('//')[1])
    return cluster, jupyter_link, client

def getAzureMLComputeCluster(ws,ct,env,login_config,pri_key_file):
    cluster = AzureMLComputeCluster(
        workspace=ws,
        compute_target=ct,
        initial_node_count=1,
        experiment_name=login_config["aml_compute"]["exp_name"],
        environment_definition=env,
        jupyter_port=login_config["aml_compute"]["jupyter_port"],
        telemetry_opt_out=login_config["azureml_user"]["telemetry_opt_out"],
        admin_username=login_config["aml_compute"]["admin_name"],
        admin_ssh_key=pri_key_file,
        )
    jupyter_link = cluster.jupyter_link
    return cluster, jupyter_link


def setUpComputeTarget(ws,login_config):
    ### experiment name
    exp_name = login_config["aml_compute"]["exp_name"]
    ### azure ml names
    ct_name = login_config["aml_compute"]["ct_name"]
    vm_priority = login_config["aml_compute"]["vm_priority"]
    vm_name = login_config["aml_compute"]["vm_name"].lower()

    ### trust but verify
    verify = f"""
    Experiment name: {exp_name}"""
    log(verify)

    verify = f"""
    Compute target: {ct_name}
    VM Size: {vm_name}
    Priority: {vm_priority}
    """
    log(verify)

    ### get SSH keys
    ssh_key_pub, pri_key_file = get_ssh_keys()

    if ct_name not in ws.compute_targets:
        logger.warning(f"Compute target {ct_name} does not exist...")
        ct = createOrGetComputeTarget(
            ws, ct_name, vm_name, vm_priority, ssh_key_pub, login_config
        )
    else:
        ct = ws.compute_targets[ct_name]

        if ct.provisioning_state == "Failed":
            logger.warning(
                f"Compute target {ct_name} found but provisioning_state is showing as 'failed'..."
            )
            logger.warning(f"Deleting {ct_name} target and will attempt again...")
            logger.warning(
                 f"If this fails again check that you have enough resources in your subscription..."
            )

            ct.delete()
            time.sleep(5)
            ct = createOrGetComputeTarget(
                ws, ct_name, vm_name, vm_priority, ssh_key_pub, login_config
            )
        else:
            log(f"    Using pre-existing compute target {ct_name}")
    return ct, pri_key_file

def get_ssh_keys():
    from cryptography.hazmat.primitives import serialization as crypto_serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.backends import default_backend as crypto_default_backend

    dir_path = os.path.join(os.getcwd(), ".ssh")

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    pub_key_file = os.path.join(dir_path, "key.pub")
    pri_key_file = os.path.join(dir_path, "key")

    keys_exist = True

    if not os.path.exists(pub_key_file):
        print("Public SSH key does not exist!")
        keys_exist = False

    if not os.path.exists(pri_key_file):
        print("Private SSH key does not exist!")
        keys_exist = False

    if not keys_exist:
        key = rsa.generate_private_key(
            backend=crypto_default_backend(), public_exponent=65537, key_size=2048
        )

        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption(),
        )
        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH,
        )

        with open(pub_key_file, "wb") as f:
            f.write(public_key)

        with open(pri_key_file, "wb") as f:
            f.write(private_key)

        os.chmod(pri_key_file, 0o600)

    with open(pub_key_file, "r") as f:
        pubkey = f.read()

    return pubkey, pri_key_file


def createOrGetComputeTarget(
    ws, ct_name, vm_name, vm_priority, ssh_key_pub, login_config
):
    config = AmlCompute.provisioning_configuration(
        vm_size=vm_name,
        min_nodes=login_config["aml_compute"]["min_nodes"],
        max_nodes=login_config["aml_compute"]["max_nodes"],
        vm_priority=vm_priority,
        idle_seconds_before_scaledown=login_config["aml_compute"][
            "idle_seconds_before_scaledown"
        ],
        admin_username=login_config["aml_compute"]["admin_name"],
        admin_user_ssh_key=ssh_key_pub,
        remote_login_port_public_access="Enabled",
    )
    ct = ComputeTarget.create(ws, ct_name, config)
    ct.wait_for_completion(show_output=True)

    if ct.provisioning_state != "Succeeded":
        msg = f"Failed to create the cluster..."
        logger.exception(msg)
        raise Exception(msg)
    return ct


def createOrGetEnvironment(ws, login_config, app_config):
    environment_name = login_config["aml_compute"]["environment_name"]
    python_interpreter = login_config["aml_compute"]["python_interpreter"]
    conda_packages = login_config["aml_compute"]["conda_packages"]

    ### CREATE OR RETRIEVE THE ENVIRONMENT
    if environment_name not in ws.environments:
        log(f"Creating {environment_name} environment...")
        env = Environment(name=environment_name)
        env.docker.enabled = login_config["aml_compute"]["docker_enabled"]
        env.docker.base_image = None
        env.docker.base_dockerfile = f'FROM {app_config["base_dockerfile"]}'
        env.python.interpreter_path = python_interpreter
        env.python.user_managed_dependencies = True
        conda_dep = CondaDependencies()

        for conda_package in conda_packages:
            conda_dep.add_conda_package(conda_package)

        env.python.conda_dependencies = conda_dep
        env.register(workspace=ws)
    else:
        log(f"    Environment {environment_name} found...")
        env = ws.environments[environment_name]

    return env

def load_content(url,targetfile,src_path,dest_path,additional_content,app_config,ws):
    tarextensions = [".tar",".tbz",".tgz",".txz"]
    if app_config["additional_content"]["download_content"]:
        if (
            "source" in additional_content.keys()
            and additional_content["source"] == "github"
        ):
            ngccontent.clone_github_repo(url,"additional_content",src_path)
            if "githubdirectory" in additional_content.keys():
                src_path = additional_content["githubdirectory"]
        else:
            lcl_path = "additional_content"
            if type(targetfile) == list:
                targetfiles = targetfile
                lcl_path = os.path.join(lcl_path,src_path)
                for targetfile in targetfiles:
                    if app_config["additional_content"]["download_content"]:
                        ngccontent.download(url+targetfile, lcl_path, targetfile)
            else:
                ngccontent.download(url, lcl_path, targetfile)
                if (
                    app_config["additional_content"]["unzip_content"]
                    and additional_content["zipped"]
                ):
                    fileroot, file_extension = os.path.splitext(targetfile)
                    if file_extension in tarextensions:
                        ngccontent.decompress_tarfile(targetfile, "additional_content", src_path)
                    else:
                        ngccontent.unzipFile(targetfile, "additional_content", src_path)
                    
    if app_config["additional_content"]["upload_content"]:
        ngccontent.upload_data(
            ws,
            ws.get_default_datastore(),
            "additional_content/" + src_path,
            dest_path,
        )

    return


def load_content_to_scheduler(url,targetfile,src_path,dest_path,additional_content,app_config,client):
    if app_config["additional_content"]["download_content"]:
        if (
            "source" in additional_content.keys()
            and additional_content["source"] == "github"
        ):
            #ngccontent.clone_github_repo(url,"additional_content",src_path)
            if "githubdirectory" in additional_content.keys():
                src_path = additional_content["githubdirectory"]
        else:
            lcl_path = src_path
            if type(targetfile) == list:
                targetfiles = targetfile
                lcl_path = dest_path
                for targetfile in targetfiles:
                    if app_config["additional_content"]["download_content"]:
                        client.run_on_scheduler(ngccontent.download,url+targetfile, lcl_path, targetfile)
            else:
                client.run_on_scheduler(ngccontent.download,url, lcl_path, targetfile) 
                if (
                    app_config["additional_content"]["unzip_content"]
                    and additional_content["zipped"]
                ):
                    log("Uploading {} content to folder {} on the scheduler".format(url,dest_path))
                    client.run_on_scheduler(ngccontent.unzipFile,targetfile, src_path, dest_path)      
    return

def go():
    start()


if __name__ == "__main__":
    go()
