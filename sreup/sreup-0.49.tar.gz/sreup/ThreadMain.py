import requests, time,os
from sreup.Client import Client
import multiprocessing
from sreup.common import config
import traceback
class ThreadMain:
    def execute(self):
        while True:
            try:
                if "1" == requests.get(config.ServerAdress.REUP_SERVER + "client/check/restart").text:
                    break
                obj = requests.get(config.ServerAdress.REUP_SERVER + "job/get", headers={"Bas-Name": "AutoWin"}).json()
                if 'id' in obj:
                    timeout = os.getenv('FF_CLIENT_TIMEOUT', config.Timeout.CLIENT)
                    client = Client(obj['id'], obj['gmail'], obj['task_list'], int(timeout))
                    client.start()
                    client.wait()
                    print('done')
                else:
                    time.sleep(config.TimeSleep.NO_JOB)
            except:
                traceback.print_exc()
                time.sleep(config.TimeSleep.EXCEPT)
                pass

    def start(self):
        self.processx = multiprocessing.Process(target=self.execute)
        self.processx.start()
    def join(self,time):
        self.processx.join(time)
    def wait(self,timeout):
        self.processx.join(timeout)
        if self.processx.is_alive():
            self.processx.terminate()
            self.processx.join()

