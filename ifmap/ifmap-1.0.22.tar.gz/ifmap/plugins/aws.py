import paramiko
from pprint import pprint
import boto3
from simple_utils import logging
from .interface import Map


class AWSMap(Map):
    def __init__(self, name, kwargs):
        super().__init__(name, kwargs)
        self._name = name
        self._kwargs = kwargs
        self._templates = None
        self._cfs = None
        self._scripts = None
        self._gits = None

        region_name = self.properteis.get('aws', {}).get('region_name', None)

        self._cf = boto3.client('cloudformation', region_name=region_name)

        self._ssm = boto3.client('ssm', region_name=region_name)

        self._ec2 = boto3.client('ec2', region_name=region_name)

    @property
    def cfs(self):
        if not self._cfs:
            self._cfs = self.get_specs('aws', 'cloudformation')
        return self._cfs

    @property
    def scripts(self):
        if not self._scripts:
            self._scripts = self.get_specs('aws', 'script')
        return self._scripts

    @property
    def gits(self):
        if not self._gits:
            self._gits = self.get_specs('aws', 'git')
        return self._gits

    def _get_stack_name(self, cf_name):
        return self.cfs[cf_name]['stack_name']

    def _read_body(self, cf_name):
        with open(self.cfs[cf_name]['path'], 'r') as fp:
            return fp.read()

    def create_stack(self, cf_name):

        return self._cf.create_stack(
            StackName=self._get_stack_name(cf_name),
            TemplateBody=self._read_body(cf_name)
        )

    def update_stack(self, cf_name):
        return self._cf.update_stack(
            StackName=self._get_stack_name(cf_name),
            TemplateBody=self._read_body(cf_name)
        )

    def delete_stack(self, cf_name):
        return self._cf.delete_stack(
            StackName=self._get_stack_name(cf_name)
        )

    def upcreate_stack(self, cf_name):
        try:
            stack = self._cf.describe_stacks(
                StackName=self._get_stack_name(cf_name))['Stacks'][0]

        except:
            logging.info(f'{cf_name} 스택을 생성합니다.')
            print(self.create_stack(cf_name))
            waitor = self._cf.get_waiter('stack_create_complete')
            print(waitor.wait(StackName=self._get_stack_name(cf_name)))
        else:
            if stack['StackStatus'] == 'ROLLBACK_COMPLETE':
                logging.info(f'{cf_name} 스택을 삭제 후 생성합니다.')
                print(self.delete_stack(cf_name))
                waitor = self._cf.get_waiter('stack_delete_complete')
                print(waitor.wait(StackName=self._get_stack_name(cf_name)))
                print(self.create_stack(cf_name))
            else:
                logging.info(f'{cf_name} 스택을 업데이트합니다.')
                print(self.update_stack(cf_name))
                waitor = self._cf.get_waiter('stack_update_complete')
                print(waitor.wait(StackName=self._get_stack_name(cf_name)))

    def execute_in_ssh(self, host, user, commands, key_pair_path):
        cli = paramiko.SSHClient()
        cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        cli.connect(host, port=22, username=user,
                    pkey=paramiko.RSAKey.from_private_key_file(key_pair_path))
        logging.info(f'{host}에 원격 명령어를 실행합니다.')
        for command in commands:
            logging.info(command)
            _, stdout, stderr = cli.exec_command(command)
            logging.info(stdout.read().decode())
            logging.warning(stderr.read().decode())

        cli.close()

    def _get_hosts(self, tag_key, tag_value):
        hosts = []
        for reservation in self._ec2.describe_instances(Filters=[{
            "Name": f'tag:{tag_key}',
            "Values": [tag_value]
        }])['Reservations']:
            hosts.extend([p['PublicDnsName']
                          for p in reservation['Instances']])
        return hosts

    def _get_commands_by_script_name(self, script_name):
        with open(self.scripts[script_name]['path'], 'r') as fp:
            return fp.read().split('\n')

    def execute(self, script_name, tag_key, tag_value, auth_name):
        commands = self._get_commands_by_script_name(script_name)
        self.execute_commands(commands, tag_key, tag_value, auth_name)

    def execute_commands(self, commands, tag_key, tag_value, auth_name):
        hosts = self._get_hosts(tag_key, tag_value)
        auth = self.properteis.get('aws', {}).get('auth', {})
        key_pair_path = auth[auth_name]['key_pair']['path']
        user = auth[auth_name]['user']

        for host in hosts:
            self.execute_in_ssh(host, user, commands, key_pair_path)

    def send_command(self, command, tag_key, tag_value, auth_name):
        self.execute_commands([command], tag_key, tag_value, auth_name)

    def git_clone(self, git_name, tag_key, tag_value, auth_name):
        url = self._gits[git_name]['url']
        install_path = self._gits[git_name]['install_path']
        self.execute_commands(
            [f'cd {install_path} && sudo git clone {url}'], tag_key, tag_value, auth_name)

    def git_pull(self, git_name, tag_key, tag_value, auth_name):
        install_path = self._gits[git_name]['install_path']
        self.execute_commands(
            [f'cd {install_path} && sudo git pull'], tag_key, tag_value, auth_name)

    def process(self):
        if self._name == 'upcreate_stack' or self._name == '1':
            self.upcreate_stack(self._kwargs['cf_name'])
        elif self._name == 'delete_stack' or self._name == '2':
            self.delete_stack(self._kwargs['cf_name'])
        elif self._name == 'execute' or self._name == '3':
            self.execute(
                self._kwargs['script_name'], tag_key=self._kwargs.get('tag_key', 'Name'), tag_value=self._kwargs['tag_value'], auth_name=self._kwargs.get('auth_name', 'default'))
        elif self._name == 'send_command' or self._name == '4':
            self.send_command(self._kwargs['command'], tag_key=self._kwargs.get(
                'tag_key', 'Name'), tag_value=self._kwargs['tag_value'], auth_name=self._kwargs.get('auth_name', 'default'))

        elif self._name == 'git_clone' or self._name == '100':
            self.git_clone(git_name=self._kwargs['git_name'], tag_key=self._kwargs.get(
                'tag_key', 'Name'), tag_value=self._kwargs['tag_value'], auth_name=self._kwargs.get('auth_name', 'default'))

        elif self._name == 'git_pull' or self._name == '101':
            self.git_pull(git_name=self._kwargs['git_name'], tag_key=self._kwargs.get(
                'tag_key', 'Name'), tag_value=self._kwargs['tag_value'], auth_name=self._kwargs.get('auth_name', 'default'))
        else:
            logging.error(f"매개변수 'kind'의 값('{self._name}')이 유효하지 않습니다.")
            exit()
