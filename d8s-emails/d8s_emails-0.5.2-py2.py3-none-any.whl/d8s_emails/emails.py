from typing import Any, Dict, List

from .emails_temp_utils import list_delete_empty_items, dict_add


def is_email(possible_email_text: str) -> bool:
    """Determine if the given string is an email."""
    # TODO (oct 2020): replace the list_delete_empty_items with iterables.remove_empty or something like that
    try:
        email_object = email_read(possible_email_text)
    except Exception:
        return False
    else:
        # make sure there is at least one body with content in the email
        email_bodies = list_delete_empty_items(email_bodies_as_strings(possible_email_text))

        if email_object.items() and any(email_bodies):
            return True
        else:
            return False


def email_header_date_fix(email_text: str):
    """Fix the `Date` header in the given email email_text."""
    import re

    date_header_pattern = 'Date: (.*)'
    date_headers = re.findall(date_header_pattern, email_text)

    # TODO: keep working on this

    for date in date_headers:
        print('date {}'.format(date))

    return date_headers


def email_read(email_string: str):
    """."""
    import email
    from email.policy import default

    return email.message_from_string(email_string, policy=default)


def email_object_new():
    """."""
    import email

    return email.message.Message()


def email_content_transfer_encoding(email_text):
    """Get the content-transfer-encoding for the email (see https://www.w3.org/Protocols/rfc1341/5_Content-Transfer-Encoding.html)."""
    # TODO: update the name and name of the argument for this function... It should be geared for bodies and attachments
    if isinstance(email_text, str):
        email_object = email_read(email_text)
    else:
        email_object = email_text

    return email_object['Content-Transfer-Encoding']


def _is_email_object(possible_email_object: Any):
    """Check if the possible_email_object is an email object."""
    import email

    return isinstance(possible_email_object, email.message.Message)


def email_bodies_as_strings(email_text):
    """Return the bodies (as strings) for the given email."""
    body_objects = email_bodies_as_objects(email_text)
    body_strings = [body.get_payload() for body in body_objects]
    return body_strings


# TODO: write a decorator to process the incoming string as an email
def email_bodies_as_objects(email_text):
    """Return the bodies (as objects) for the given email."""
    if isinstance(email_text, str):
        email_object = email_read(email_text)
    else:
        email_object = email_text

    body_objects = []

    if email_object.is_multipart():
        for subpart in email_object.get_payload():
            body_objects.extend(email_bodies_as_objects(subpart))
    else:
        if email_object.get_content_disposition() != "attachment":
            body_objects.append(email_object)

    return body_objects


def email_attachments(email_text):
    """Return the attachments (as strings) for the given email."""
    attachment_objects = email_attachments_objects(email_text)
    attachment_strings = [attachment.get_payload() for attachment in attachment_objects]
    return attachment_strings


def email_attachments_objects(email_text):
    """Return the attachments (as objects) for the given email."""
    if isinstance(email_text, str):
        email_object = email_read(email_text)
    else:
        email_object = email_text

    attachment_objects = []

    if email_object.is_multipart():
        for subpart in email_object.get_payload():
            attachment_objects.extend(email_attachments_objects(subpart))
    else:
        if email_object.get_content_disposition() == "attachment":
            attachment_objects.append(email_object)

    return attachment_objects


def email_body_is_base64(email_text):
    """Determine if the body of the email is encoded using base64."""
    # TODO: update this function to take a body object as an argument - there should also be a parallel function for attachments
    return email_content_transfer_encoding(email_text) == 'base64'


def email_header_fields(email_text):
    """Get the header fields in the email."""
    if isinstance(email_text, str):
        email_object = email_read(email_text)
    else:
        email_object = email_text

    return email_object.keys()


def email_headers(email_text):
    """Get the values of the header fields in the email."""
    if isinstance(email_text, str):
        email_object = email_read(email_text)
    else:
        email_object = email_text

    return email_object.items()


def email_headers_raw(email_text):
    """Get the raw (undecoded) values of the header fields in the email."""
    if isinstance(email_text, str):
        email_object = email_read(email_text)
    else:
        email_object = email_text

    return [item for item in email_object.raw_items()]


def email_headers_as_dict(email_text) -> Dict[str, List[str]]:
    """Return email's header fields as a dictionary with the header field key as the dictionary's key and the header field value as the dictionary's value."""
    headers = email_headers(email_text)
    email_header_dict = {}

    for key, value in headers:
        dict_add(email_header_dict, key, value)

    return email_header_dict


def email_header(email_text, header_field):
    """Get the value(s) for the given header fields."""
    if isinstance(email_text, str):
        email_object = email_read(email_text)
    else:
        email_object = email_text

    return email_object.get_all(header_field)


def email_header_delete_field(email_text, header_field):
    """Delete the header_field from the email_text."""
    # TODO: make a copy of the email_object before deleting an element from it
    if isinstance(email_text, str):
        email_object = email_read(email_text)
    else:
        email_object = email_text

    del email_object[header_field]
    return email_object


def _email_structure_iterator(email_object, email_structure=None):
    """Iterate through the given email_object and find its structure. This function is called from the `emailStructure` function."""
    if email_structure is None:
        email_structure = {}

    email_structure['type'] = email_object.get_content_type()
    email_structure['content_disposition'] = email_object.get_content_disposition()
    email_structure['children'] = []

    if email_object.is_multipart():
        for subpart in email_object.get_payload():
            email_structure['children'].append(_email_structure_iterator(subpart))

    return email_structure


def email_structure(email_text):
    """Get the structure of the email (this function was inspired by the function here: https://github.com/python/cpython/blob/4993cc0a5b34dc91da2b41c50e33d809f0191355/Lib/email/iterators.py#L59 - which is described here: https://docs.python.org/3.5/library/email.iterators.html?highlight=_structure#email.iterators._structure)."""
    if isinstance(email_text, str):
        email_object = email_read(email_text)
    else:
        email_object = email_text

    return _email_structure_iterator(email_object)


def email_header_add_raw(email, header_name, header_value):
    """Add a header to the email."""
    if isinstance(email, str):
        email_object = email_read(email)
    else:
        email_object = email

    email_object.set_raw(header_name, header_value)
    return email_object


def email_header_add(email, header_name, header_value):
    """Add a header to the email."""
    if isinstance(email, str):
        email_object = email_read(email)
    else:
        email_object = email

    email_object.add_header(header_name, header_value)
    return email_object
