from django.conf import settings
from django.core.mail import send_mail

from singular_server_management.management.commands.server_base_command import ServerBaseCommand

PROJECT_NAME = getattr(settings, 'PROJECT_NAME', '')
HOST = getattr(settings, 'HOST', '')
USER = getattr(settings, 'USER', '')
GIT_PASSWORD = getattr(settings, 'GIT_PASSWORD', '')
PASSWORD = getattr(settings, 'PASSWORD', '')
KEY_FILE = getattr(settings, 'KEY_FILE', '')

if PASSWORD:
    UPDATE_CRONJOB = ('1 0 * * *', 'django.core.management.call_command',
                      [
                          f'update_server {PROJECT_NAME} {HOST} {USER} {GIT_PASSWORD} --server_password {PASSWORD}']),
else:
    UPDATE_CRONJOB = ('1 0 * * *', 'django.core.management.call_command',
                      [
                          f'update_server {PROJECT_NAME} {HOST} {USER} {GIT_PASSWORD} --key_file {KEY_FILE}']),


class Command(ServerBaseCommand):
    help = 'Update test server'

    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)
        try:
            with self.connection.cd(f'/var/www/django_apps/{self.project_name}/{self.project_name}'):
                self.update_project()
            self.restart_services()
        except Exception as e:
            send_mail(f'Failed to update {self.host} on project {self.project_name}', str(e),
                      settings.DEFAULT_FROM_EMAIL,
                      settings.ADMINS)
