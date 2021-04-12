
import json
import nvgpu
import docker
import logging
import platform
import requests
import subprocess
from os.path import expanduser, join, exists

OAUTH_API_URL = 'https://api.nanami.io/oauth'
# QUEUE_API_URL = 'https://api.nanami.io/queue'
QUEUE_API_URL = 'http://localhost:5000'

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)

def container_stop(containers):
    for container in containers:
        if container:
            container.stop()
            logger.info(f"{container}: is stopped.")

def container_run(client, arguments, command, setup_command=None):
    container = client.containers.create(**arguments)

    logger.info(f'Image : {arguments["image"]} is now starting in {container}!')

    container.start()
    try:
        nanami_setup_log = container.exec_run('pip install -U nanami', stream=True, tty=True, environment=["PYTHONUNBUFFERED=0"])
        for line in nanami_setup_log[1]:
            logger.info(line.decode('utf-8').strip())

        if setup_command:
            setup_log = container.exec_run(setup_command, stream=True, tty=True, environment=["PYTHONUNBUFFERED=0"])
            for line in setup_log[1]:
                logger.info(line.decode('utf-8').strip())

        exec_log = container.exec_run(command, stream=True, tty=True, environment=["PYTHONUNBUFFERED=0"])
        for line in exec_log[1]:
            logger.info(line.decode('utf-8').strip())

    except KeyboardInterrupt as e:
        logger.info(f'Container will be stopped!')
        container_stop([container])

def check_arguments(data, arguments):
    errors = []
    for _argument in arguments:
        if _argument not in data:
            errors.append(f"Argument({_argument}) is not found.")
    if errors:
        raise NotImplementedError(errors)

def check_auth():
    path = join(expanduser("~"), '.nanami.json')
    if not exists(path):
        raise FileNotFoundError("Please `nanami login` first.")
    with open(path) as fp:
        user = json.load(fp)
    return user

def check_entrypoint(entrypoint):
    with open(entrypoint) as f:
        start, end = False, False
        for line in f.read().splitlines():
            line = line.strip()
            if "nanami.start()" == line:
                start = True
            if "nanami.end()" == line:
                end = True
    return (start and end)

def docker_version_check():
    client = docker.from_env()
    version = [int(v) for v in client.version()['Components'][0]['Version'].split('.')]
    assert version[0] >= 19 and version[1] >= 3

def find_image_in_local(image):
    client = docker.from_env()
    images = []
    for _image in client.images.list():
        images.extend(_image.tags)
    if image in images:
        return True
    else:
        return False

def gpu_check(gpus='', verbose=False):
    if gpus == '':
        return None

    device_requests = []
    nvidia_smi = parse_nvidia_smi()
    if nvidia_smi:
        cuda_version = nvidia_smi['CUDA Version']
        if gpus == 'all':
            gpus = nvgpu.available_gpus()
            device_requests = [
                docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])
            ]
        else:
            device_requests = []
            gpu_uuid = dict({g['index'] : g['uuid'] for g in nvgpu.gpu_info()})
            for g_idx in gpus.split(','):
                if g_idx not in [g['index'] for g in nvgpu.gpu_info()]:
                    raise NotImplementedError(f"Device id({g_idx}) is avaliable.")
                elif g_idx not in nvgpu.available_gpus():
                    raise NotImplementedError(f"Device id({g_idx}) is using.")
                device_requests.extend([
                    docker.types.DeviceRequest(
                        driver='nvidia',
                        device_ids=[gpu_uuid[g_idx]],
                        capabilities=[
                            ['gpu']
                        ]
                    )
                ])
        if gpus:
            client = docker.from_env()
            nvidia_smi = client.containers.run(
                f'nvidia/cuda:{cuda_version}-base',
                'nvidia-smi',
                remove=True,
                device_requests=device_requests
            )
            if verbose:
                print(nvidia_smi.decode('utf-8'))
        else:
            device_requests = []
            logger.info('All GPUs is using.')

    return device_requests

def image_search(image):
    sp = subprocess.Popen(
        ['docker', 'inspect', '--type=image', image], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out_str = sp.communicate()
    out_json = json.loads(out_str[0].decode("utf-8"))
    if out_json:
        return True
    else:
        return False

def image_pulling(image):
    completed_process = subprocess.run(
        ['docker', 'pull', image], input=None, stdout=None, stderr=None
    )
    if completed_process.returncode != 0:
        raise NotImplementedError(f"Pulling Error : {image}")

def nvidia_docker_version_check():
    try:
        sp = subprocess.Popen(['nvidia-docker', 'version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out_str = sp.communicate()
        out_list = out_str[0].decode("utf-8").split('\n')

        out_dict = {}

        for item in out_list:
            try:
                key, val = item.split(':')
                key, val = key.strip(), val.strip()
                out_dict[key] = val
            except:
                pass

        version = [int(v) for v in out_dict['NVIDIA Docker'].split('.')]
        assert version[0] >= 2 and version[1] >= 5
    except:
        logger.warning("nvidia-docker is not installed.")

def parse_nvidia_smi():
    try:
        sp = subprocess.Popen(['nvidia-smi', '-q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        return None

    out_str = sp.communicate()
    out_list = out_str[0].decode("utf-8").split('\n')

    out_dict = {}

    for item in out_list:
        try:
            key, val = item.split(':')
            key, val = key.strip(), val.strip()
            out_dict[key] = val
        except:
            pass

    return out_dict

def post(path, data):
    r = requests.post(path, json=data)
    if r.status_code == 200:
        return r.json()
    else:
        return None