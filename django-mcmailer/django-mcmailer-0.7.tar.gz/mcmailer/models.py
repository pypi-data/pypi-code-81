from django.db import models
from django.utils.safestring import mark_safe


class SystemFromEmailAddress(models.Model):
    email = models.EmailField()
    from_official_name = models.CharField(
        max_length=255,
        help_text="This is the text that it gets displayed when "
                  "viewing the email from the email list on your email client."
    )
    code_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "System From Email Address"
        verbose_name_plural = "System From Email Address"

    def __str__(self):
        return "{}".format(self.email)


class EmailNotificationRecipient(models.Model):
    email = models.EmailField()

    class Meta:
        verbose_name_plural = "Email Notification Recipients"

    def __str__(self):
        return "{}".format(self.email)


class EmailTemplate(models.Model):
    name = models.CharField(max_length=255)
    preview_text = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    plain_body = models.TextField()
    html_body = models.TextField()

    def html_body_preview(self):
        if self.html_body:
            return mark_safe('<div id="html_preview"></div>')
        else:
            return 'N/A'

    html_body_preview.short_description = 'HTML preview'
    html_body_preview.allow_tags = True

    def __str__(self):
        return "{}".format(self.name)


class GmailConnectionToken(models.Model):
    json_string = models.TextField()
    valid = models.BooleanField()
    gmail_address = models.EmailField()

    def __str__(self):
        return self.gmail_address
