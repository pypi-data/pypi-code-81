from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.

from emails.email_helpers import send_user_email
from emails import scheduling

"""
TEST STUFF
"""


def send_test(request, *args, **kwargs):

    send_user_email(request.user, 'welcome')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), '/')

def start_email_scheduler(request, *args, **kwargs):

    scheduling.start()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), '/')
