from django.core.management import BaseCommand
from fabric import Connection
from invoke import Responder


class ServerBaseCommand(BaseCommand):
    str_params = ['project_name', 'host', 'user', 'git_user_password']
    optional_str_params = ['--server_password', '--key_file']
    optional_bool_params = ['--websocket', '--cronjob']
    host = None
    user = None
    server_password = None
    key_file = None
    project_name = None
    git_user_password = None
    has_websockets = None
    has_cronjobs = None
    connection = None

    def restart_services(self):
        self.connection.run(f'systemctl restart gunicorn_{self.project_name}')
        print('gunicorn restarted')
        self.connection.run('systemctl restart nginx')
        print('nginx restarted')
        if self.has_websockets:
            self.connection.run('systemctl restart daphne')
            print('daphne restarted')

    def add_arguments(self, parser):
        for arg in self.str_params:
            parser.add_argument(arg, nargs='?', type=str)
        for arg in self.optional_bool_params:
            parser.add_argument(arg, nargs='?', type=bool)
        for arg in self.optional_str_params:
            parser.add_argument(arg, nargs='?', type=str)

    def make_migrations(self, initial=False):
        if initial:
            output = self.connection.run(
                'source ../env/bin/activate && python manage.py makemigrations core && python manage.py makemigrations  && python manage.py migrate')
        else:
            output = self.connection.run(
                'source ../env/bin/activate && python manage.py makemigrations && python manage.py migrate')

        self.show_output(output)

    def get_static_files(self):
        static_response = Responder(pattern="Type 'yes' to continue, or 'no' to cancel:", response='yes\n')
        output = self.connection.run(
            'source ../env/bin/activate python manage.py collectstatic',
            pty=True, watchers=[static_response])
        self.show_output(output)

    def get_new_files(self):
        git_password = Responder(pattern="Password for 'https://LucasLGsing@bitbucket.org':",
                                 response=f'{self.git_user_password}\n')
        output = self.connection.run('git pull', pty=True, watchers=[git_password])
        self.show_output(output)

    def enable_cronjobs(self):
        if self.has_cronjobs:
            self.connection.run(
                'source ../env/bin/activate && python manage.py crontab remove && python manage.py crontab add')

    def update_project(self):
        self.get_new_files()
        self.make_migrations()
        self.get_static_files()
        self.enable_cronjobs()
        self.connection.run(
            f'source env/bin/activate && pip3 install -r {self.project_name}/requirements.txt')

    def show_output(self, output):
        for line in output.stdout.split("\r\n"):
            print(line)

    def get_params(self, kwargs):
        print(kwargs)
        self.project_name = kwargs['project_name']
        self.host = kwargs['host']
        self.user = kwargs['user']
        self.git_user_password = kwargs['git_user_password']
        if kwargs['server_password']:
            self.server_password = kwargs['server_password']
        if kwargs['key_file']:
            self.key_file = kwargs['key_file']

        self.has_websockets = kwargs.get('websockets', None)
        self.has_cronjobs = kwargs.get('cronjobs', None)

    def handle(self, *args, **kwargs):
        self.get_params(kwargs)
        conn_kwargs = {'password': self.server_password} if self.server_password else {'key_filename': self.key_file}
        self.connection = Connection(host=self.host, user=self.user, port=22,
                                     connect_kwargs=conn_kwargs)
