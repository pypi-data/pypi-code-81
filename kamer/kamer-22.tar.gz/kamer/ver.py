# kamer/version.py
#
#

""" version plugin. """

__version__ = 22

txt = "OTP-CR-117/19 otp.informationdesk@icc-cpi.int http://pypi.org/project/genocide !"

def ver(event):
    event.reply(txt)
