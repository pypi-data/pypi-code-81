from datetime import timedelta
from django.utils import timezone
from emails import email_helpers
from apscheduler.schedulers.background import BackgroundScheduler
from config.settings.base import EMAIL_CHECK_INTERVAL, PROGRAM_NAME
from django.core.mail import send_mail
from config.settings.base import ALERT_EMAIL_ADDRESSES




def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_emails, 'interval', hours=EMAIL_CHECK_INTERVAL)
    scheduler.start()
    print('Starting email scheduler...')


def schedule_emails():
    from .models import EmailSchedule

    last_email_sent_record = EmailSchedule.objects.get_last_email_sent()
    last_email_sent = last_email_sent_record.last_email_sent
    send_time = timezone.now()

    admin_email_msg = ''
    admin_email_times = '<strong>Start time:</strong> ' + str(last_email_sent) + '<br/><strong>End time:</strong> ' + str(send_time) + '<br/><br/>'

    """SCHEDULED EMAILS"""

    email_code = 'trial-expiring-today'
    users_emailed = schedule_user_emails(email_code, last_email_sent, send_time, 28)
    admin_email_msg = update_admin_email(admin_email_msg, users_emailed, email_code)

    email_code = 'trial-expired'
    users_emailed = schedule_user_emails(email_code, last_email_sent, send_time, 29)
    admin_email_msg = update_admin_email(admin_email_msg, users_emailed, email_code)

    if len(admin_email_msg) > 0:
        admin_email_msg = admin_email_times + admin_email_msg
        send_mail('Scheduled ' + PROGRAM_NAME + ' Email Report', admin_email_msg, email_helpers.SEND_ADDRESS,  ALERT_EMAIL_ADDRESSES, html_message=admin_email_msg)

    EmailSchedule.objects.update_last_email_sent(send_time)


def schedule_user_emails(email_id, last_email_sent, send_time, days):
    from users.models import User

    start_time = last_email_sent - timedelta(days=days)
    end_time = send_time - timedelta(days=days)

    users_since_last_check = User.objects.get_users_signed_up_between(start_time, end_time)


    print(start_time)
    print(end_time)
    print(users_since_last_check)

    for email_user in users_since_last_check:
        email_helpers.send_user_email(email_user, email_id)

    return users_since_last_check


def update_admin_email(email_msg, users_emailed, email_id):

    if len(users_emailed) > 0:

        email_msg += '<h4>' + email_id + '</h4>'
        for user in users_emailed:
            email_msg += user.username + '<br/>'

        email_msg += '<br/>'

    return email_msg
