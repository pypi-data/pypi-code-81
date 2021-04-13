#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
# import certifi
from requests_toolbelt import MultipartEncoder

# 重点是这个cookie， 没有的话会被阿里的套件拦截
url = "https://www.ncbi.nlm.nih.gov/protein/AYO18310?report=fasta"

# data = {"file" : open("/home/nobel/Downloads/example.pdb", "rb")}

file = ""
# data 参数
# demo: yes
# MAX_FILE_SIZE: 3000000
# upload: (binary)
# sbut: Use Demo File
# eMail: 2097227267@qq.com
# job-name:
# MAX_FILE_SIZE: 3000000
# ref: (binary)
# MAX_FILE_SIZE: 3000000
# con: (binary)
# lownstruct: 100
# highnstruct: 100
# columns[]: total_score
# columns[]: rmsBB
# file = MultipartEncoder(
#     fields={
#             # 'field0': 'value',
#             # 'field1': 'value',
#             'upload': ('file', open("/home/nobel/Downloads/example.pdb", "rb"), 'application/file'),
#             # 'filed3': ("aab.jpg", open("aab.jpg", 'rb'), "image/jpeg")
# })

def post(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cache-Control":"max-age=0",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Referer":"http://flexpepdock.furmanlab.cs.huji.ac.il/index.php",
        "Host": "flexpepdock.furmanlab.cs.huji.ac.il",
        "Origin":"http://flexpepdock.furmanlab.cs.huji.ac.il",
        "Upgrade-Insecure-Requests":"1",
        "Proxy-Connection":"keep-alive",
    }
    # , verify = certifi.where()
    # result = requests.get(url, headers=headers, data={}, verify=certifi.where(),timeout=30)
    result = requests.post(url,  headers={"Content-Type":file.content_type},data=file)
    return result

# 从单个的开始做,然后再批量
def atom_task(pdb_url):
    global file
    file = MultipartEncoder(
        fields={
            # 'field0': 'value',
            # 'field1': 'value',
            'upload': ('file', open(pdb_url, "rb"), 'application/file'),
            # 'filed3': ("aab.jpg", open("aab.jpg", 'rb'), "image/jpeg")
        })
    res = post('http://flexpepdock.furmanlab.cs.huji.ac.il/saveFile.php').text
    # 这里要把结果号爬出来

    if res.__contains__("You did not succeed in uploading the PDB fil"):
        print("failed, may be the format of your pdb file is wrong")
    else:
        soup = BeautifulSoup(res, "lxml")
        for x in soup.find_all("td"):
            if x.get('id') is not None:
                if x.get('id') == 'content':
                    result_url = x.find_all('a')[1].get('href')
                    # print(x.find_all('a')[1].get('href'))
        print("success, the result url is " + result_url)


# if __name__ == '__main__':
#     atom_task("/home/nobel/Downloads/example.pdb")
    # atom_task("/home/nobel/Downloads/example.pdb")
    # res = post('http://flexpepdock.furmanlab.cs.huji.ac.il/saveFile.php').text
    # print( res)
    # if res.__contains__("You did not succeed in uploading the PDB fil"):
    #     print("failed")
    # else:
    #     print("success")
    # print(get('http://flexpepdock.furmanlab.cs.huji.ac.il/script.js').text)



