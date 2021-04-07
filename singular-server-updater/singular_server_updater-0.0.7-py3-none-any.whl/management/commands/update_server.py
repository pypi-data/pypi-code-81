from django.core.management import BaseCommand
from fabric import Connection
from invoke import Responder


class Command(BaseCommand):
    help = 'Update test server'
    str_params = ['project_name', 'host', 'user', 'server_password', 'git_user_password']
    bool_params = ['has_websockets', 'has_cronjobs']

    def add_arguments(self, parser):
        for arg in self.str_params:
            parser.add_argument(arg, nargs='+', type=str)
        for arg in self.bool_params:
            parser.add_argument(arg, nargs='?', type=bool, default=False)

    def show_output(self, output):
        for line in output.stdout.split("\r\n"):
            print(line)

    def handle(self, *args, **kwargs):
        host = kwargs['host'][0]
        user = kwargs['user'][0]
        server_password = kwargs['server_password'][0]
        git_user_password = kwargs['git_user_password'][0]
        project_name = kwargs['project_name'][0]
        has_websockets = kwargs['has_websockets']
        has_cronjobs = kwargs['has_cronjobs']

        try:
            connection = Connection(host=host, user=user, port=22,
                                    connect_kwargs={'password': server_password})
            with connection.cd(f'/var/www/django_apps/{project_name}/{project_name}'):
                git_password = Responder(pattern="Password for 'https://LucasLGsing@bitbucket.org':",
                                         response=f'{git_user_password}\n')
                static_response = Responder(pattern="Type 'yes' to continue, or 'no' to cancel:", response='yes\n')
                output = connection.run('git pull', pty=True, watchers=[git_password])
                self.show_output(output)
                output = connection.run(
                    'source ../env/bin/activate && python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic',
                    pty=True, watchers=[static_response])
                self.show_output(output)
                if has_cronjobs:
                    connection.run(
                        'source ../env/bin/activate && python manage.py crontab remove && python manage.py crontab add')
            connection.run(f'systemctl restart gunicorn_{project_name}')
            print('gunicorn restarted')
            connection.run('systemctl restart nginx')
            print('nginx restarted')
            if has_websockets:
                connection.run('systemctl restart daphne')
                print('daphne restarted')


        except Exception as e:
            print(e)
