from django.db import models

class EmailScheduleManager(models.Manager):

    def get_last_email_sent(self):
        return self.all().order_by('-id')[0]

    def update_last_email_sent(self, new_start_time):

        last_email_sent_record = self.all().order_by('-id')[0]
        last_email_sent_record.last_email_sent = new_start_time
        last_email_sent_record.save()


class EmailSchedule(models.Model):
    last_email_sent = models.DateTimeField()

    objects = EmailScheduleManager()

    def __str__(self):
        return str(self.last_email_sent)
