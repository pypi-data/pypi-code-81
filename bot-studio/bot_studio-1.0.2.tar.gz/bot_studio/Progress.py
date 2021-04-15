from tqdm import tqdm
import requests
import time
import json
def fetch_progress(user,bot,indexnumber,api):
    data={"user":user,"bot":bot,"indexnumber":indexnumber}
    headers = {'Content-type': 'application/json'}
    res=requests.post(url = api, data = json.dumps(data), headers=headers)
    res=res.text
    res=json.loads(res)
    return res["progress"]
def show_progress(user,bot,indexnumber,api):
    prog=5
    last=5
    with tqdm(total=200, desc="Progress") as progress:
        progress.update(10)
        while(prog!=100):
            last=prog
            prog=fetch_progress(user,bot,indexnumber,api)
            time.sleep(2)
            if(prog==0 or prog<=5):
                pass
            else:
                final=prog-last
                progress.update(final+final)
    progress.close()
