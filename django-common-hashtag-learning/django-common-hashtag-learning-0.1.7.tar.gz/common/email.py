from config.settings.base import PROGRAM_NAME, ALERT_EMAIL_ADDRESSES
from django.core.mail import send_mail

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from config.settings.base import SEND_IN_BLUE_API_KEY, SEND_IN_BLUE_LIST_ID

def new_school_email(user, school_name, authority, school_type):
    msg = 'There is a new account sign up' + '\n\n'
    msg += "Program: " + PROGRAM_NAME + '\n'
    msg += 'School: ' + school_name + '\n'
    msg += 'Authority: ' + authority.authority_name + '\n'
    msg += 'School Type: ' + school_type + '\n\n'

    msg += 'User: ' + user.first_name + ' ' + user.last_name + '\n'
    msg += 'Email: ' + user.email

    send_mail("New " + PROGRAM_NAME + " Sign Up", msg,
              "Hashtag Learning<contact@hashtag-learning.co.uk>", ALERT_EMAIL_ADDRESSES)


def new_user_existing_school_email(user, school):
    msg = 'There is a new account sign up to an existing school account' + '\n\n'
    msg += "Program: " + PROGRAM_NAME + '\n'
    msg += 'School: ' + school.school_name + '\n'

    msg += 'User: ' + user.first_name + ' ' + user.last_name + '\n'
    msg += 'Email: ' + user.email

    send_mail("New " + PROGRAM_NAME + " Sign Up (Existing School)", msg,
              "Hashtag Learning<contact@hashtag-learning.co.uk>", ALERT_EMAIL_ADDRESSES)

def add_send_in_blue_contact(user):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = SEND_IN_BLUE_API_KEY

    email = user.username
    first_name = user.first_name
    last_name = user.last_name
    school = user.school.school_name

    # create an instance of the API class
    api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
    list_id = SEND_IN_BLUE_LIST_ID
    create_contact = sib_api_v3_sdk.CreateContact(email=email,)
    contact_email = sib_api_v3_sdk.AddContactToList([email])

    update_contact = sib_api_v3_sdk.UpdateContact({'LASTNAME': last_name, 'FIRSTNAME': first_name, 'SCHOOL': school})


    try:
        api_instance.create_contact(create_contact)
        api_instance.update_contact(email, update_contact)

    except ApiException as e:
        print("Exception when calling ContactsApi->create contact: %s\n" % e)

    try:
        api_instance.add_contact_to_list(list_id, contact_email)
    except ApiException as e:
        print("Exception when calling ContactsApi->add_contact_to_list: %s\n" % e)
