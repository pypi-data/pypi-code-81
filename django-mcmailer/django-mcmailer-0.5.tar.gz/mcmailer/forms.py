from django import forms

from mcmailer.models import EmailTemplate


class SendTestEmailForm(forms.Form):
    from_email_address = forms.EmailField()
    from_official_name = forms.CharField(required=False)
    to_email_address = forms.EmailField()
    subject = forms.CharField(required=False)
    body = forms.CharField(widget=forms.Textarea, required=False)
    template_to_use = forms.ModelChoiceField(
        queryset=EmailTemplate.objects.all(),
        empty_label="Nothing",
        help_text='If a template is used, then the From official name, Subject and Body will '
                  'be overridden with the template\'s variables.'
    )
