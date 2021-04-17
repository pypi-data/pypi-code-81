import os
class ServerAdress(object):
    MAIL_SERVER = "http://178.128.211.227"
    REUP_SERVER = "http://sreup.singerchart.com/"
class ImageResource(object):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    ICON_GOOGLE=dir_path+"/res/google.png"
    ICON_PUBLIC=dir_path+"/res/public.png"
    UPLOAD_BUTTON=dir_path+"/res/upload_button.png"
    RECOVERY_MAIL=dir_path+"/res/confirm_email.png"
class Client(object):
    EXT=".exe"
    ROOT_FOLDER=""
class Timeout(object):
    CLIENT=1800
    THREAD=90000
class TimeSleep(object):
    NO_JOB=60
    EXCEPT=30