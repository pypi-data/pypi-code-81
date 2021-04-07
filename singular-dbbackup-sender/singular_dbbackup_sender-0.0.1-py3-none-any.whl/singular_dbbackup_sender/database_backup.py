from django.conf import settings

BACKUP_CRONJOB = ('0 */8 * * *', 'singular_database_backup.database_backup.generate_backup', '>> /var/log/crontab/crontab.log'),

def generate_backup():
    import os
    from django.core.mail import EmailMessage
    from django.core.management import call_command

    try:
        call_command('dbbackup')
        backup_path = os.path.join(settings.BACKUP_FOLDER, settings.DBBACKUP_FILENAME_TEMPLATE)
        backup_name = settings.DBBACKUP_FILENAME_TEMPLATE
        email = EmailMessage(backup_name, '', settings.DEFAULT_FROM_EMAIL, settings.EMAILS_BACKUP)
        with open(backup_path, 'r') as file:
            email.attach(f'{backup_name}', file.read())
        email.send()
        os.remove(backup_path)
    except Exception as e:
        print(e)
