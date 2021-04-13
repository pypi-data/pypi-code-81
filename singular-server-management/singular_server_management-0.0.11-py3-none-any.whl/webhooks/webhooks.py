import json

from django.conf import settings
from django.core.mail import send_mail
from django.core.management import call_command
from django.http import HttpResponse
from django.views.generic.base import View

FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL', 'system@singular.inf.br')
TO_EMAIL = getattr(settings, 'ADMINS', [('Ivan', 'ivan@singular.inf.br')])


class PushRequest(View):
    def post(self, *args, **kwargs):
        status = 200
        server_settings = settings.SERVER_SETTINGS
        email_title = f'Server update status at {server_settings["PROJECT_NAME"]}-{server_settings["HOST"]}'
        try:
            body = json.loads(self.request.body.decode('utf-8'))
            branch_name = body['push']['changes'][0]['new']['name']
            if branch_name == settings.SERVER_BRANCH:
                if server_settings.get('PASSWORD', None):
                    call_command('update_project', server_settings['PROJECT_NAME'], server_settings['HOST'],
                                 server_settings['USER'],
                                 server_settings['GIT_PASSWORD'], server_password=server_settings["PASSWORD"])
                else:
                    call_command('update_project', server_settings['PROJECT_NAME'], server_settings['HOST'],
                                 server_settings['USER'],
                                 server_settings['GIT_PASSWORD'], key_file=server_settings["KEY_FILE"])
                send_mail(email_title,
                          'Server updated successfully!', FROM_EMAIL, TO_EMAIL)
        except Exception as e:
            status = 500
            send_mail(email_title, str(e),
                      FROM_EMAIL, TO_EMAIL)
        return HttpResponse(status=status)
