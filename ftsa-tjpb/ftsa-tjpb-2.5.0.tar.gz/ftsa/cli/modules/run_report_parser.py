import os
import socket
from datetime import datetime
from ftsa.cli.utils.files import delete_path, delete_file, is_project_ftsa, get_project_properties
from ftsa.cli.modules.properties import IMAGE_NAME, IMAGE_VERSION


RESULTS_DIRECTORIES = [
    'results',
    'output',
    'pabot_results',
    'report',
    'dist',
    'videos'
]

FILES = [
    '.pabotsuitenames',
    'log.html',
    'report.html',
    'output.xml'
]


def add_tags(args, tipo):
    if hasattr(args, tipo) and getattr(args, tipo) is not None:
        return ' '.join(['--' + tipo + ' ' + i for i in getattr(args, tipo)])
    return ''


def docker_report(args):
    is_project_ftsa()
    clear(args)
    include = add_tags(args, 'include')
    exclude = add_tags(args, 'exclude')

    if hasattr(args, 'pull') and getattr(args, 'pull'):
        os.system(f'docker pull {IMAGE_NAME}:{IMAGE_VERSION}')
    else:
        os.system(f'docker build -t {IMAGE_NAME}:{IMAGE_VERSION} ./')

    grid_name = f'{datetime.now().strftime("%Y%m%d%H%M%S")}_grid'
    if hasattr(args, 'net') and getattr(args, 'net') is not None:
        grid_name = getattr(args, 'net')
    os.system(f'docker network create {grid_name}')

    user_exec_container = 'execution_robot'
    if hasattr(args, 'container') and getattr(args, 'container') is not None:
        user_exec_container = getattr(args, 'container')

    host = socket.gethostbyname(socket.gethostname())
    if hasattr(args, 'dockerhost') and getattr(args, 'dockerhost') is not None:
        host = getattr(args, 'dockerhost')

    cmd = f'docker run --name {user_exec_container} --net {grid_name} ' \
          f'-v "{os.getcwd()}":/opt/robotframework/tests ' \
          f'-v /var/run/docker.sock:/var/run/docker.sock ' \
          f'-e SELENIUM_EXEC_HOST={host} ' \
          f'-e USER_GRID_NAME={grid_name} ' \
          f'-e USER_EXEC_CONTAINER={user_exec_container} ' \
          f'{IMAGE_NAME}:{IMAGE_VERSION} ' \
          f'bash && ftsa report {include}{exclude}'
    print(f'{cmd}')
    os.system(cmd)
    os.system(f'docker stop {user_exec_container} && docker rm {user_exec_container}')
    os.system(f'docker network rm {grid_name}')


def report(args):
    is_project_ftsa()
    clear(args)
    include = add_tags(args, 'include')
    exclude = add_tags(args, 'exclude')

    parallel = 1
    if hasattr(args, 'parallel') and getattr(args, 'parallel') is not None and int(getattr(args, 'parallel')) > 1:
        parallel = int(args.parallel)
    project = get_project_properties()
    try:
        quantity = project.get('prop', 'PARALLEL')
        if quantity is not None and int(quantity) > 1:
            parallel = int(project.get('prop', 'PARALLEL'))
            print(f'A propriedade PARALLEL foi definida no arquivo de propriedades: {parallel}')
    except:
        print('A propriedade PARALLEL não existe no arquivo de propriedades do projeto')

    options = f'--verbose --testlevelsplit'
    if hasattr(args, 'allure') and getattr(args, 'allure') is not None and getattr(args, 'allure'):
        os.system(f'pabot {options} --processes {parallel} --listener allure_robotframework '
                  f'--outputdir ./output {include}{exclude} --timestampoutputs ./features')
        os.system(f'allure serve ./output/allure')
    elif parallel == 1:
        os.system(f'robot -d ./output {include}{exclude} --timestampoutputs ./features')
    else:
        os.system(f'pabot {options} --processes {parallel} --outputdir ./output {include}{exclude} --timestampoutputs ./features')


def clear(args):
    is_project_ftsa()
    for directory in RESULTS_DIRECTORIES:
        delete_path(os.path.join(os.getcwd(), directory))
    for file in FILES:
        delete_file(os.path.join(os.getcwd(), file))


def run(args):
    report(args)
    clear(args)
