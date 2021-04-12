
import json
import click
from flask import Flask, request
from urllib.parse import urlparse

from nanami.utils import *
from nanami.nanami import Nanami

proxy_container = None
app = Flask(__name__)

docker_version_check()
nvidia_docker_version_check()

def create_app():
    @app.route('/')
    def index():
        return 'Nanami Test'

    @app.route('/message', methods=['POST'])
    def message():
        data = request.get_json()
        check_arguments(data, ["project", "status"])
        logger.info(f'[{data["status"]}]: {data["project"]}')

    @app.route('/running', methods=['POST'])
    def running():
        data = request.get_json()
        check_arguments(data, ["project"])

        port = urlparse(data['project']['localhost']).port
        dequeuing(QUEUE_API_URL, apikey=data['project']['apikey'], port=port)

    return app

def dequeuing(QUEUE_API_URL, apikey, port):
    dequeue_result = post(f"{QUEUE_API_URL}/dequeue", data={'apikey': apikey})
    if dequeue_result:
        if dequeue_result['success']:
            queue_info = dequeue_result['queue_info']
            running(
                image=queue_info['image'],
                workspace=queue_info['workspace'],
                entrypoint=queue_info['entrypoint'],
                gpus=queue_info['gpus'],
                argument=queue_info['argument'],
                cache=queue_info['cache'],
                queue_id=queue_info['queue_id'],
                apikey=apikey,
                port=port
            )
        else:
            if dequeue_result['message']:
                print(f'Failed to dequeue : {(dequeue_result["message"])}.')
            else:
                print(f'Failed to dequeue.')
    else:
        print(f'[API Error] : {QUEUE_API_URL}/dequeue')

def running(image, workspace, entrypoint, gpus, argument, cache, queue_id=None, apikey=None, port=None):
    nanami = Nanami(image, workspace, entrypoint, gpus, argument, cache, queue_id)
    if queue_id and apikey and port:
        nanami.save(apikey=apikey, port=port)

    if not find_image_in_local(image=image):
        image_pulling(image=image)

    run_argument = {
        'image': image,
        'command': "/bin/bash",
        'volumes': {nanami.workspace: {'bind': '/workspace', 'mode': 'rw'}},
        'working_dir': '/workspace',
        'tty': True,
        'stdin_open': True,
    }

    client = docker.from_env()
    if nanami.device_requests:
        logger.info('[GPU mode]')
        run_argument.update({'device_requests': nanami.device_requests})
        container_run(client=client, arguments=run_argument, command=nanami.command, setup_command=nanami.setup_command)
    else:
        if gpus:
            logger.warning("You are running with GPU mode but All GPUs is working.")
        logger.info('[CPU mode]')
        container_run(client=client, arguments=run_argument, command=nanami.command, setup_command=nanami.setup_command)

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if not ctx.invoked_subcommand:
        pass

@cli.command()
@click.option('--gpus', '-g', type=str, default='all', help='GPU number ex) 0,1')
def gpu(gpus):
    gpu_check(gpus=gpus, verbose=True)

@cli.command()
@click.option('--image', '-i', type=str, required=True, help='Docker image name')
@click.option('--workspace', '-w', type=str, required=True, help='Workspace directory path')
@click.option('--entrypoint', '-e', type=str, required=True, help='Entrypoint filename')
@click.option('--gpus', '-g', type=str, default='', help='GPU number ex) 0,1')
@click.option('--argument', '-a', type=str, default='')
@click.option('--cache', '-c', is_flag=True, help="Caching Docker image")
# TODO: caching mechanism with docker image build
def local(image, workspace, entrypoint, gpus='', argument='', cache=False):
    running(image, workspace, entrypoint, gpu, argument, cache)

@cli.command()
def queue():
    user = check_auth()
    queue_list = post(f"{QUEUE_API_URL}/queue", data={
        'apikey': user['user']['apikey'],
    })
    if queue_list:
        if queue_list['success']:
            print(f'enqueue succeeded : {queue_list["queue_list"]}')
        else:
            print('enqueue failed.')
    else:
        print(f'[API Error] : {QUEUE_API_URL}/queue.')

@cli.command()
@click.option('--image', '-i', type=str, required=True, help='Docker image name')
@click.option('--workspace', '-w', type=str, required=True, help='Workspace directory path')
@click.option('--entrypoint', '-e', type=str, required=True, help='Entrypoint filename')
@click.option('--gpus', '-g', type=str, default='', help='GPU number ex) 0,1')
@click.option('--argument', '-a', type=str, default='')
@click.option('--cache', '-c', is_flag=True, help="Caching Docker image")
def add(image, workspace, entrypoint, gpus='', argument='', cache=False):
    user = check_auth()
    Nanami(image, workspace, entrypoint, gpus, argument, cache)
    enqueue_result = post(f"{QUEUE_API_URL}/add", data={
        'apikey' : user['user']['apikey'],
        'image': image,
        'workspace': workspace,
        'entrypoint': entrypoint,
        'gpus': gpus,
        'argument': argument,
        'cache': cache
    })
    if enqueue_result:
        if enqueue_result['success']:
            print(f'enqueue succeeded : {enqueue_result["queue_id"]}.')
        else:
            print('enqueue failed.')
    else:
        print(f'[API Error] : {QUEUE_API_URL}/add.')

@cli.command()
@click.option('--id', type=str, required=True, help='Queue id')
def rm(id):
    user = check_auth()
    remove_result = post(f"{QUEUE_API_URL}/remove", data={
        'apikey': user['user']['apikey'],
        'queue_id': id
    })
    if remove_result:
        if remove_result['success']:
            print(f'Successful removal of queue_id({id}).')
        else:
            print(f'Failed to remove queue_id({id}).')
    else:
        print(f'[API Error] : {QUEUE_API_URL}/remove.')

@cli.command()
@click.option('--port', type=int, default=7007, help='')
def start(port):
    user = check_auth()
    path = join(expanduser("~"), '.nanami.json')
    with open(path, 'w') as fp:
        json.dump({'user': user['user'], 'port': port}, fp, indent=4)
    apikey = user['user']['apikey']

    dequeuing(QUEUE_API_URL, apikey, port)

    app = create_app()
    app.run('0.0.0.0', port=port)

@cli.command()
@click.option('--apikey', type=str, default=None,
    help='You can find your API key in your browser here: https://nanami.io/')
def login(apikey):
    if apikey:
        user = post(f"{OAUTH_API_URL}/check", data={'apikey': apikey})
        if user:
            if user['success']:
                user = json.loads(user['user'])
                print(f"Welcome {user['github_login']}!")
                path = join(expanduser("~"), '.nanami.json')
                with open(path, 'w') as fp:
                    json.dump({'user': user}, fp, indent=4)
            else:
                print('Authentication is fail.')
        else:
            print(f'[API Error] : {OAUTH_API_URL}/check')
    else:
        print('`apikey` should not `None`. "Try nanami login --help" for help.')