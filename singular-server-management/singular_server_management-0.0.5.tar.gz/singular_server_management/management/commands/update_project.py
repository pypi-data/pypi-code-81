from django.conf import settings
from django.core.mail import send_mail

from singular_server_management.management.commands.server_base_command import ServerBaseCommand

UPDATE_CRONJOB = ('1 0 * * *', 'django.core.management.call_command',
                  [
                      f'update_server {settings.SERVER_SETTINGS["PROJECT_NAME"]} {settings.SERVER_SETTINGS["HOST"]} {settings.SERVER_SETTINGS["USER"]} {settings.SERVER_SETTINGS["PASSWORD"]} {settings.SERVER_SETTINGS["GIT_PASSWORD"]}']),


class Command(ServerBaseCommand):
    help = 'Update test server'
    str_params = ['project_name', 'host', 'user', 'server_password', 'git_user_password']
    bool_params = ['has_websockets', 'has_cronjobs']

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
