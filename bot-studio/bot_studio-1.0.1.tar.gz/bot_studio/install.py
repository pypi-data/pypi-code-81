import subprocess
import os
import time
import json
import requests
import platform
def get_chrome_version():
    process = subprocess.Popen(
        ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
    )
    version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
    version=version.split(".")[0]
    return version
def installdatakund():
    version=get_chrome_version()
    url="http://127.0.0.1:5350/install"
    headers = {'Content-type': 'application/json'}
    api_data={"userid":"","browser":"chrome","majorVersion":version,"tech_type":"PIP"}
    res=requests.post(url = url, data = json.dumps(api_data), headers=headers)
    res=json.loads(res.text)
def startdatakund(folderpath):
    try:
        installdatakund()
        return 0
    except:
        dirpath=folderpath+"DataKund.exe"
        print("Starting DataKund...")
        os.startfile(dirpath)
    i=0
    while(i<120):
        try:
            installdatakund()
            break
        except:
            time.sleep(1)
        i=i+1
def checkifinstall(folderpath):
    ostype=platform.system()
    if("Windows" in ostype):
        startdatakund(folderpath)
        serverurl="http://127.0.0.1:5350/"
    else:
        serverurl=""
    return serverurl