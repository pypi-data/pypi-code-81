import requests
import json
import os

class Downloader:

    @staticmethod
    def get(url):
        r = requests.get(url)
        return r.text

    @staticmethod
    def download(_to,_from,_what,_back):
        result = json.loads(Downloader.get("https://raw.githubusercontent.com/"
                                           "New-Vektor-Group/pkg-repo/main/"+_back+"/libs.json"))

        if(_what not in result.keys()):
            return False

        pkg = result[_what]
        text = Downloader.get(_from+pkg["package"]+".php")

        if(pkg["isfile"]):
            with open(_to + pkg["package"] + "." + _back, "w") as f:
                f.write(text)
        else:
            folder = _to + pkg["package"]
            os.mkdir(folder)
            github_api = "https://api.github.com/repos/New-Vektor-Group/pkg-repo/contents/php/" \
                         ""+pkg["package"]

            r = requests.get(github_api).text
            r = json.loads(r)
            for i in r:
                if i["type"] == "file":
                    with open(folder + "/" + i["name"], "w") as f:
                        text = Downloader.get(_from + pkg["package"] + "/" + i["name"])
                        f.write(text)
                else:
                    os.mkdir(folder+"/"+i["name"])
                    r2 = requests.get(github_api+"/"+i["name"]).text
                    r2 = json.loads(r)
                    for j in r2:
                        if j["type"] == "file":
                            with open(folder + "/" + i["name"] + "/" + j["name"], "w") as f:
                                text = Downloader.get(_from + pkg["package"] + "/" + i["name"] + "/" + j["name"])
                                f.write(text)

        if(len(pkg["dep"]) > 0):
            for d in pkg["dep"].values():
                with open(_to + d + "." + _back, "w") as f:
                    textd = Downloader.get(_from + d + ".php")
                    f.write(textd)