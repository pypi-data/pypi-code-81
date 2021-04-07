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
        email_message = 'Server updated successfully!'
        try:
            body = json.loads(self.request.body.decode('utf-8'))
            branch_name = body['push']['changes']['new']['name']
            if branch_name == settings.SERVER_BRANCH:
                server_settings = settings.SERVER_SETTINGS
                generate_backup()
                call_command('update_server', server_settings['PROJECT_NAME'], server_settings['HOST'],
                             server_settings['USER'], server_settings['PASSWORD'],
                             server_settings['GIT_PASSWORD'], server_settings.get('HAS_WEBSOCKETS', False),
                             server_settings.get('HAS_CRONJOBS', False))
        except Exception as e:
            status = 500
            email_message = str(e)
        finally:
            send_mail('Server update status', email_message, settings.DEFAULT_FROM_EMAIL, settings.ADMINS)
        return HttpResponse(status=status)
