import requests
import os
import tempfile
import datetime,shutil
from sreup.common import config
__all__ =["load_cookie","save_cookie"]

def get_dir(dir):
    tmp_download_path = os.path.join(tempfile.gettempdir(), dir)
    if not os.path.exists(tmp_download_path):
        os.makedirs(tmp_download_path)
    return tmp_download_path

def make_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
def load_cookie(cookie_folder,email):
    api_address = os.getenv("MAIL_SERVER", config.ServerAdress.MAIL_SERVER)
    r = requests.get(api_address+"/automail/api/cookie/get/"+email)
    make_folder(cookie_folder)
    with open(cookie_folder+"/cookies.sqlite", 'wb') as f:
        f.write(r.content)

def save_cookie(cookie_folder,email):
    with open(cookie_folder+"/cookies.sqlite", 'rb') as f:
        files = {'file':('cookies.sqlite',f)}
        data={'fileName':email}
        api_address=os.getenv("MAIL_SERVER", config.ServerAdress.MAIL_SERVER)
        requests.post(api_address+"/automail/api/mail/upload/", data=data,files=files)
def call_success(server_address,job_id,gmail,video_id):
    log_data="s;;"+ str(datetime.datetime.now())+";;"+gmail+";;"+video_id;
    data={'id':job_id,'log_data':log_data}
    requests.post(server_address,data=None,json=data)
def clear_data():
    cmd= "rm -rf "+get_dir('download')
    try:
        shutil.rmtree(get_dir('download'))
    except:
        os.system(cmd)
        pass
def unlock_process(server_address,job_id):
    log_data="f;;"+ str(datetime.datetime.now());
    data={'id':job_id,'log_data':log_data}
    requests.post(server_address,data=None,json=data)

def call_error(server_address,job_id,gmail,log):
    log_data="e;;"+ str(datetime.datetime.now())+";;"+gmail+";;"+log;
    data={'id':job_id,'log_data':log_data}
    requests.post(server_address,data=None,json=data)
    
def get_video():
    return requests.get("http://news.singerchart.com/msn/link/get").text;


