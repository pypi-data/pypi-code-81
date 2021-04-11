from modeltranslation.translator import register, TranslationOptions

from mcmailer.models import EmailTemplate


@register(EmailTemplate)
class DoorSystemTranslationOptions(TranslationOptions):
    fields = ('subject', 'preview_text', 'plain_body', 'html_body',)
