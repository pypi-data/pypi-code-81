from os import walk

from django.conf import settings

BACKUP_CRONJOB = ('0 */8 * * *', 'singular_dbbackup_sender.database_backup.generate_backup',
                  '>> /var/log/crontab/crontab.log'),


def generate_backup():
    import os
    from django.core.mail import EmailMessage
    from django.core.management import call_command

    try:
        call_command('dbbackup')
        backup_path = settings.DBBACKUP_STORAGE_OPTIONS['location']
        files = []
        for file_path in os.listdir(backup_path):
            email = EmailMessage(f'Generated backup from {settings.APP_NAME.upper()}', '', settings.DEFAULT_FROM_EMAIL,
                                 getattr(settings, 'EMAILS_BACKUP', settings.ADMINS))
            with open(os.path.join(backup_path,file_path), 'r',  encoding='iso8859-1') as file:
                split_path = os.path.split(file.name)
                file_name = split_path[-1]
                file_content = file.read()
                email.attach(f'{file_name}', file_content)
            email.send()
            files.append(os.path.join(backup_path,file_path))
        for f in files:
            os.remove(f)
    except Exception as e:
        print(e)
