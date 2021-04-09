from django.conf import settings

BACKUP_CRONJOB = ('0 */8 * * *', 'singular_database_backup.database_backup.generate_backup',
                  '>> /var/log/crontab/crontab.log'),


def generate_backup():
    import os
    from django.core.mail import EmailMessage
    from django.core.management import call_command

    try:
        call_command('dbbackup')
        backup_path = settings.DBBACKUP_STORAGE_OPTIONS['location']
        email = EmailMessage(f'Generated backup from {settings.APP_NAME.upper()}', '', settings.DEFAULT_FROM_EMAIL,
                             getattr(settings, 'EMAILS_BACKUP', settings.ADMINS))
        with open(f'{backup_path}', 'r+') as file:
            file_name = file.name.split("/")[-1]
        email.attach(f'{file_name}', file.read())
        email.send()
        os.remove(backup_path)
    except Exception as e:
        print(e)
