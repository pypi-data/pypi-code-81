import json

from django.conf import settings
from django.core.mail import send_mail
from django.core.management import call_command
from django.http import HttpResponse
from django.views.generic.base import View
from singular_dbbackup_sender.database_backup import generate_backup


class PushRequest(View):
    def post(self, *args, **kwargs):
        status = 200
        server_settings = settings.SERVER_SETTINGS
        email_title = f'Server update status at {server_settings["PROJECT_NAME"]}-{server_settings["HOST"]}'
        try:
            body = json.loads(self.request.body.decode('utf-8'))
            branch_name = body['push']['changes'][0]['new']['name']
            if branch_name == settings.SERVER_BRANCH:
                generate_backup()
                call_command('update_server', server_settings['PROJECT_NAME'], server_settings['HOST'],
                             server_settings['USER'], server_settings['PASSWORD'],
                             server_settings['GIT_PASSWORD'], server_settings.get('HAS_WEBSOCKETS', False),
                             server_settings.get('HAS_CRONJOBS', False))
                send_mail(email_title,
                          'Server updated successfully!', settings.DEFAULT_FROM_EMAIL, settings.ADMINS)
        except Exception as e:
            status = 500
            send_mail(email_title, str(e),
                      settings.DEFAULT_FROM_EMAIL, settings.ADMINS)
        return HttpResponse(status=status)
