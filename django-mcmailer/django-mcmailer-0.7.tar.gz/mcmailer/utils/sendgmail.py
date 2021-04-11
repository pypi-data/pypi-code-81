import base64
import datetime
import json
import mimetypes
import os
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import google.auth.transport.requests
import google.auth.transport.requests
import google.oauth2.credentials
import google.oauth2.credentials
from apiclient import errors, discovery

from mcmailer.models import GmailConnectionToken


def send_message(credentials, sender, to, subject, msg_html, msg_plain, attachment_file=None):
    service = discovery.build('gmail', 'v1', credentials=credentials)
    if attachment_file:
        message1 = create_message_with_attachment(sender, to, subject, msg_html, msg_plain, attachment_file)
    else:
        message1 = create_message_html(sender, to, subject, msg_html, msg_plain)
    result = send_message_internal(service, "me", message1)
    return result


def send_message_internal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"


def create_message_html(sender, to, subject, msg_html, msg_plain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msg_plain, 'plain'))
    if msg_html:
        msg.attach(MIMEText(msg_html, 'html'))
    return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}


def create_message_with_attachment(sender, to, subject, msg_html, msg_plain, attachment_file):
    """Create a message for an email.
    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      msg_html: Html message to be sent
      msg_plain: Alternative plain text message for older email clients
      attachment_file: The path to the file to be attached.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEMultipart('mixed')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    messageA = MIMEMultipart('alternative')
    messageR = MIMEMultipart('related')

    if msg_html:
        messageR.attach(MIMEText(msg_html, 'html'))
    messageA.attach(MIMEText(msg_plain, 'plain'))
    messageA.attach(messageR)

    message.attach(messageA)

    print("create_message_with_attachment: file: %s" % attachment_file)
    content_type, encoding = mimetypes.guess_type(attachment_file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(attachment_file, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(attachment_file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(attachment_file, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(attachment_file, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(attachment_file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}


def save_credentials(gmail_address, credentials, valid=True):
    try:
        creds = GmailConnectionToken.objects.get(gmail_address=gmail_address)
    except GmailConnectionToken.DoesNotExist:
        creds = GmailConnectionToken()
        creds.gmail_address = gmail_address
    temp = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'id_token': credentials.id_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'expiry': datetime.datetime.strftime(credentials.expiry, '%Y-%m-%d %H:%M:%S')
    }
    creds.json_string = json.dumps(temp)
    creds.valid = valid
    creds.save()
    return temp


def load_credentials(gmail_address, ignore_valid=False):
    try:
        creds = GmailConnectionToken.objects.get(gmail_address=gmail_address)
        # is it valid? do we raise an error?
        if not ignore_valid and not creds.valid:
            raise ValueError('Credentials are not valid.')
        # ok, if we get to here we load/create the Credentials obj()
        temp = json.loads(creds.json_string)
        credentials = google.oauth2.credentials.Credentials(
            temp['token'],
            refresh_token=temp['refresh_token'],
            id_token=temp['id_token'],
            token_uri=temp['token_uri'],
            client_id=temp['client_id'],
            client_secret=temp['client_secret'],
            scopes=temp['scopes'],
        )
        expiry = temp['expiry']
        expiry_datetime = datetime.datetime.strptime(expiry, '%Y-%m-%d %H:%M:%S')
        credentials.expiry = expiry_datetime
        # and now we refresh the token
        # but not if we know that its not a valid token.
        if creds.valid:
            request = google.auth.transport.requests.Request()
            if credentials.expired:
                credentials.refresh(request)
        # and finally, we return this whole deal
        if ignore_valid:
            return True, credentials, creds.valid
        else:
            return True, credentials

    except GmailConnectionToken.DoesNotExist:
        error_message = 'The Gmail address "{}" has not authorized the application to send emails'.format(gmail_address)
        return False, error_message


def send_mc_email(credentials, from_address, to_addresses, from_official_name, subject, msg_plain, msg_html=None,
                  attachment_file=None):
    sender = "{} <{}>".format(from_official_name, from_address)
    to_addresses = ', '.join(to_addresses)
    if attachment_file:
        send_message(credentials, sender, to_addresses, subject, msg_html, msg_plain, attachment_file)
    else:
        send_message(credentials, sender, to_addresses, subject, msg_html, msg_plain)
