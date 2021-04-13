import os

from django.conf import settings
from django.core.mail import send_mail
from invoke import Responder, UnexpectedExit

from singular_server_management.management.commands.server_base_command import ServerBaseCommand


class Command(ServerBaseCommand):
    SERVICES_FOLDER = '/etc/systemd/system/'
    NGINX_FOLDER = '/etc/nginx/sites-available/'
    help = 'Update test server'
    str_params = ['project_name', 'host', 'port', 'user', 'git_user_password']
    files_path = f'{os.path.dirname(__file__)}/../../file_templates'

    def send_email(self):
        send_mail(f'Failed to build {self.host} on project {self.project_name}', str(e),
                  settings.DEFAULT_FROM_EMAIL,
                  settings.ADMINS)

    def get_params(self, kwargs):
        super(Command, self).get_params(kwargs)
        self.project_port = kwargs['port']

    def upload_temp_file(self, name, content, location):
        filename = f'{self.files_path}/{name}'
        with open(filename, 'w') as temp:
            try:
                temp.write(content)
            except Exception as e:
                print(e)
        try:
            self.connection.put(filename, location)
        except:
            pass
        try:
            self.connection.run(f'sudo systemctl enable {location}{name}')
        except:
            pass
        try:
            os.remove(filename)
        except:
            pass

    def configure_gunicorn(self):
        try:
            socket_file = open(f'{self.files_path}/gunicorn_default.socket', 'r')
            service_file = open(f'{self.files_path}/gunicorn_default.service', 'r')
            socket_content = socket_file.read()
            service_content = service_file.read()
            socket_content = socket_content.replace('default', self.project_name)
            service_content = service_content.replace('default', self.project_name)
            self.upload_temp_file(f'gunicorn_{self.project_name}.socket', socket_content, self.SERVICES_FOLDER)
            self.upload_temp_file(f'gunicorn_{self.project_name}.service', service_content, self.SERVICES_FOLDER)
        except Exception as e:
            print(e)

    def configure_daphne(self):
        try:
            service_file = open(f'{self.files_path}/daphne.service', 'r')
            service_content = service_file.read()
            service_content = service_content.replace('default', self.project_name)
            self.upload_temp_file(f'daphne.service', service_content, self.SERVICES_FOLDER)
        except Exception as e:
            print(e)

    def configure_nginx(self):
        try:
            nginx_file = open(f'{self.files_path}/nginx_file')
            nginx_content = nginx_file.read()
            nginx_content = nginx_content.replace('default', self.project_name).replace('port',
                                                                                        self.project_port).replace(
                'host', self.host)
            try:
                self.upload_temp_file(self.project_name, nginx_content, self.NGINX_FOLDER)
            except:
                pass
            try:
                self.connection.run(
                    f' sudo ln -s /etc/nginx/sites-available/{self.project_name} /etc/nginx/sites-enabled/{self.project_name}')
            except:
                pass
        except Exception as e:
            print(e)

    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)
        try:
            self.connection.run(f'cd /var/www/django_apps/{self.project_name}')
        except:
            try:
                self.connection.run(f'mkdir /var/www/django_apps/{self.project_name}')
            except:
                self.connection.run(f'mkdir /var/www/django_apps')
                self.connection.run(f'mkdir /var/www/django_apps/{self.project_name}')
                print('PLEASE MAKE THE INITIAL CONFIGURATION OF THE SERVER')
                print(
                    'RUN sudo apt install git python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl')
                return
        with self.connection.cd(f'/var/www/django_apps/{self.project_name}/'):
            try:
                git_clone_responder = Responder(pattern="Password for 'https://LucasLGsing@bitbucket.org':",
                                                response=f'{self.git_user_password}\n')
                self.connection.run(f'git clone https://LucasLGsing@bitbucket.org/singular-dev/{self.project_name}.git',
                                    pty=True,
                                    watchers=[git_clone_responder])
            except UnexpectedExit as e:
                print(e)
                if 'already exists and is not an empty directory' in e.result.stdout:
                    pass
                else:
                    return
            try:
                self.connection.run(f'cd env/')
            except:
                self.connection.run(f'virtualenv env')
                pass
            with self.connection.cd(f'/var/www/django_apps/{self.project_name}/{self.project_name}'):
                self.connection.run(f'git checkout {getattr(settings, "SERVER_BRANCH", "server")}')
                self.connection.run(
                    f'source ../env/bin/activate && pip3 install -r requirements.txt')
                self.configure_gunicorn()
                if self.has_websockets:
                    self.configure_daphne()
                self.configure_nginx()
                self.connection.run(f'sudo systemctl daemon-reload')
                try:
                    self.make_migrations(True)
                    self.get_static_files()
                except Exception as e:
                    print(e)
                    print(
                        'PLEASE ACCESS THE SERVER TO ADD THE ENVIRONMENT FILE AND ASSOCIATE THE DATABASE')
                    return
        print(
            '!!!!!!!!!!!!!!!!IF REDIS,DAPHNE AND GUNICORN ARE NOT IN YOU REQUIREMENTS, PLEASE INSTALL THEM MANUALLY!!!!!!!!!!!!!!!!!!!!!!')
        print('PROJECT BUILT SUCCESSFULLY!')
        print('AFTER THAT, PLEASE RESTART ALL THE SERVICES')
