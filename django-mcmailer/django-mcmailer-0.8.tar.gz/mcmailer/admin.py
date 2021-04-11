from django.contrib import admin

from mcmailer.models import SystemFromEmailAddress, EmailNotificationRecipient, EmailTemplate, GmailConnectionToken


@admin.register(SystemFromEmailAddress)
class NotificationEmailAddressAdmin(admin.ModelAdmin):
    list_display = ('email', 'from_official_name',)
    search_fields = ('email', 'from_official_name',)


@admin.register(EmailNotificationRecipient)
class EmailNotificationRecipientAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    readonly_fields = ('html_body_preview',)

    class Media:
        js = (
            'mcmailer/mcmailer_main.js',
        )


@admin.register(GmailConnectionToken)
class GmailConnectionTokenAdmin(admin.ModelAdmin):
    pass
