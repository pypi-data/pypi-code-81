from .interface import Map
import subprocess
import simple_utils
from simple_utils import logging

class DockerMap(Map):
    def __init__(self, name, kwargs):
        super().__init__(name, kwargs)
        self._name = name
        self._kwargs = kwargs
        self._templates = None
        self._apps = None
        self._composes = None

    @property
    def apps(self):
        if not self._apps:
            self._apps = self.get_specs('docker', 'app')
        return self._apps

    @property
    def composes(self):
        if not self._composes:
            self._composes = self.get_specs('docker', 'compose')
        return self._composes

    def build_all_dockers(self):
        for app_name in self.apps.keys():
            self.build_docker(app_name)

    def build_dockers_with_template_name(self, name):
        spec = self.tm.get_spec(name)
        for app_name in spec['apps'].keys():
            self.build_docker(app_name)

    def build_docker(self, app_name):
        info = self.apps[app_name]
        docker_name = info['docker_name']
        dockerfile_dir = info['dockerfile_dir']
        simple_utils.shell.dynamic_check_output(
            f'cd {dockerfile_dir} && docker build --tag {docker_name} .')

    def remove_all_container(self):
        simple_utils.shell.dynamic_check_output(f'docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)')

    def compose_one(self, compose_name):
        path = self.composes[compose_name]['dir']
        simple_utils.shell.dynamic_check_output(f'cd {path} && docker-compose down && docker-compose up -d')

    def build_and_compose(self, app_name, compose_name):
        self.build_docker(app_name)
        self.compose_one(compose_name)

    def compose_down(self, compose_name):
        path = self.composes[compose_name]['dir']
        simple_utils.shell.dynamic_check_output(f'cd {path} && docker-compose down')
    
    def process(self):
        
        if self._name == 'build_all_dockers' or self._name == '1':
            self.build_all_dockers()

        elif self._name == 'build_dockers_with_template_name' or self._name == '2':
            self.build_dockers_with_template_name(self._kwargs['template_name'])

        elif self._name == 'build_dockers_with_app_name' or self._name == '3':
            self.build_docker(self._kwargs['app_name'])

        elif self._name == 'remove_all_container' or self._name == '4':
            self.remove_all_container()

        elif self._name == 'compose_one' or self._name == '100':
            self.compose_one(self._kwargs['compose_name'])

        elif self._name == 'build_and_compose' or self._name == '101':
            self.build_and_compose(self._kwargs['app_name'], self._kwargs['compose_name'])

        elif self._name == 'compose_down' or self._name == '102':
            self.compose_down(self._kwargs['compose_name'])
        else:
            logging.error(f"매개변수 'kind'의 값('{self._name}')이 유효하지 않습니다.")
            exit()
