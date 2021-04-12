import json

from django.conf import settings
from django.core.mail import send_mail
from django.core.management import call_command
from django.http import HttpResponse
from django.views.generic.base import View


class PushRequest(View):
    def post(self, *args, **kwargs):
        status = 200
        server_settings = settings.SERVER_SETTINGS
        email_title = f'Server update status at {server_settings["PROJECT_NAME"]}-{server_settings["HOST"]}'
        try:
            body = json.loads(self.request.body.decode('utf-8'))
            branch_name = body['push']['changes'][0]['new']['name']
            if branch_name == settings.SERVER_BRANCH:
                if server_settings['PASSWORD']:
                    call_command('update_server', server_settings['PROJECT_NAME'], server_settings['HOST'],
                             server_settings['USER'],
                             server_settings['GIT_PASSWORD'], f'--server_password {server_settings["PASSWORD"]}')
                else:
                    call_command('update_server', server_settings['PROJECT_NAME'], server_settings['HOST'],
                                 server_settings['USER'],
                                 server_settings['GIT_PASSWORD'], f'--key_file {server_settings["KEY_FILE"]}')
                send_mail(email_title,
                          'Server updated successfully!', settings.DEFAULT_FROM_EMAIL, settings.ADMINS)
        except Exception as e:
            status = 500
            send_mail(email_title, str(e),
                      settings.DEFAULT_FROM_EMAIL, settings.ADMINS)
        return HttpResponse(status=status)
