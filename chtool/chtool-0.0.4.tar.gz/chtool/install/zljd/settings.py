import configparser
import json ,os

class mysetting:

    def __init__(self):
        cf=configparser.ConfigParser()
        path=os.path.expanduser('~/.bstpasswd.ini')
        if path=='C:\\Windows\\system32\\config\\systemprofile/.bstpasswd.ini':
            path="C:\\Users\\Administrator\\.bstpasswd.ini"
        cf.read(path,encoding="utf8")

        locs=[w[4:] for w in filter(lambda x:x.startswith("loc:"),cf.sections())]

        cfg={}
        for loc in locs:
            x=cf["loc:%s"%loc]
            tmp={}
            for  k,v in x.items():
                k,v=k.strip(),v.strip()
                try:
                    tmp[k]=json.loads(v)
                except:
                    tmp[k]=v
            cfg[loc]=tmp


        self.cfg=cfg


    def __getitem__(self,loc):

        return self.cfg[loc]

    # def __setitem__(self,loc):
    #     self.cfg

gp_settings=mysetting()