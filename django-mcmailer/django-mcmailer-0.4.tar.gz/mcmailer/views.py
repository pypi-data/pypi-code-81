import os

import google_auth_oauthlib.flow
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from mcmailer.forms import SendTestEmailForm
from mcmailer.models import SystemFromEmailAddress
from mcmailer.utils.sendgmail import save_credentials, load_credentials, send_mc_email

API_SCOPE = ['https://www.googleapis.com/auth/gmail.send', ]


def get_error_msg(var_name):
    return 'Requested setting {0}, but settings are not configured. ' \
           'You must define the variable {0} in your settings.py'.format(var_name)


try:
    JSON_PATH = settings.JSON_PATH
except AttributeError:
    raise ImproperlyConfigured(get_error_msg('JSON_PATH'))
try:
    LOCAL_HOST = settings.LOCAL_HOST
except AttributeError:
    raise ImproperlyConfigured(get_error_msg('LOCAL_HOST'))

if LOCAL_HOST:
    try:
        REDIRECT_URI = settings.LOCAL_HOST_REDIRECT_URI
    except AttributeError:
        raise ImproperlyConfigured(get_error_msg('LOCAL_HOST_REDIRECT_URI'))
    # we don't have ssl on local host
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
else:
    try:
        REDIRECT_URL = settings.PRODUCTION_REDIRECT_URI
    except AttributeError:
        raise ImproperlyConfigured(get_error_msg('PRODUCTION_REDIRECT_URI'))

GMAIL_SESSION_NAME = 'gmail_session_name'


def save_email_address_to_tmp_file(gmail_address):
    with open(os.path.join(os.getcwd(), "gmail_address.tmp"), "w") as tmp_file:
        tmp_file.write(gmail_address)


def get_email_address_from_tmp_file():
    tmp_file_path = os.path.join(os.getcwd(), "gmail_address.tmp")
    with open(tmp_file_path, "r") as tmp_file:
        gmail_address = tmp_file.read()
    os.remove(tmp_file_path)
    return gmail_address


@login_required
def connect_gmail(request):
    if request.method == "POST":
        gmail_address = request.POST.get('email')
        save_email_address_to_tmp_file(gmail_address)
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(JSON_PATH, scopes=API_SCOPE)
        flow.redirect_uri = REDIRECT_URI
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            login_hint=gmail_address,
            include_granted_scopes='true'
        )
        return HttpResponseRedirect(authorization_url)
    context = {
        'email_addresses': SystemFromEmailAddress.objects.all()
    }
    return render(request, 'auth_gmail_address.html', context)


@login_required
def g_auth_endpoint(request):
    gmail_address = get_email_address_from_tmp_file()
    state = request.GET.get('state', None)
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(JSON_PATH, scopes=API_SCOPE, state=state)
    flow.redirect_uri = REDIRECT_URI
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    temp = save_credentials(gmail_address, credentials)
    return HttpResponse("Successful authorization of the gmail address {}".format(gmail_address))


def parse_template(text, objects):
    """
    Loop through the object's attributes and find all the variables in the 'text' that have
    the name of the attribute surrounded with the prefix and suffix
    and replace them with the value of the object's attribute.

    :param text: A str to replace the variables found from the objects attributes.
    :param objects: A list of objects
    :return: str the parsed text.
    """
    special_variable_prefix = '(%%'
    special_variable_suffix = '%%)'
    for obj in objects:
        for attr in dir(obj):
            template_variable = "{}{}{}".format(special_variable_prefix, attr, special_variable_suffix)
            if template_variable in text:
                text = text.replace(template_variable, getattr(obj, attr))
    return text


def send_test_email(request):
    if request.method == 'POST':
        form = SendTestEmailForm(request.POST)
        if form.is_valid():
            # Send the email
            system_from_email_address = SystemFromEmailAddress.objects.first()

            from_address = form.cleaned_data['from_email_address']
            success, credentials = load_credentials(from_address)

            to_address = form.cleaned_data['to_email_address']

            if form.cleaned_data['template_to_use']:
                email_template = form.cleaned_data['template_to_use']
                from_official_name = parse_template(
                    text=email_template.from_official_name,
                    objects=[system_from_email_address]
                )
                subject = parse_template(
                    text=email_template.subject,
                    objects=[system_from_email_address]
                )
                body = parse_template(
                    text=email_template.html_body,
                    objects=[system_from_email_address]
                )
            else:
                from_official_name = form.cleaned_data['from_official_name']
                subject = form.cleaned_data['subject']
                body = form.cleaned_data['body']

            send_mc_email(
                credentials,
                from_address=from_address,
                to_addresses=[to_address],
                from_official_name=from_official_name,
                subject=subject,
                msg_plain=body,
                msg_html=body
            )
            return HttpResponse('Email successfully sent!')
    else:
        form = SendTestEmailForm()
        context = {
            'send_test_email_form': form
        }
        return render(request, 'send_test_email.html', context)
