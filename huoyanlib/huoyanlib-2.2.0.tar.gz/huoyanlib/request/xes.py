import json
import requests
import tkinter
from tkinter import filedialog


class XesWork:
    def __init__(self, work_id):
        self.url = 'https://code.xueersi.com/api/compilers/v2/{}?id={}'.format(work_id, work_id)
        self.headers = {'Content-Encoding': 'gzip',
                        'Content-Type': 'application/json',
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-encoding': 'gzip, deflate, br',
                        'Cookie': '__guid=83032836.2463553885053085000.1588600148802.7158; hideShadeAdv=true; xesId=167d6ef5e04074cfab39d4ba07fba97d; is_login=1; stu_id=23350237; stu_name=23350237; userGrade=8; xes-code-id=d8bbb2b0b1824a169645f5660f1e9ae7.0258883033257fd3b25cfd6d76573efd; xes_acc=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOiIyMzM1NDcxOCIsInVzZXJfaWQiOiIyMzM1MDIzNyIsInJvbGUiOjEsImV4cCI6MTYwMDYwODkxOSwidmVyIjoiMS4wIn0.nWLlBnj_RELHH8w2lW-FA4PdB-J29zTIjAvPs2hZ05hsbU6zJAHMOen5HJCYe2DAXIrDE0He6Ga7q71AAblFUstcM-0WN4cP9qfR7H9dx2VaiIGmv3r58A1MFGt6dUVl1rNlEelQEhsglPhJl9A4uJuYfXJZVT-r9Opc4ik18kTbuVompBDQFf9Q11zJhhEkEGnigZ8tUhSRJabXQVd5V7JiMLJ4obOwiC-_ye4vRKJB30wEq1Y0OQQGaI40nDT8TDvgW_7d-cS7Ur5UR9XQkrfpZmnK9ogoPZ8Fu90KC7jE55OyKJ4WmC4VsQtMJjbjZIexvEdZ7URMCDY9ueRzbw; Hm_lvt_a8a78faf5b3e92f32fe42a94751a74f1=1601704217,1601814999,1601901328,1602060578; user-select=python; Hm_lpvt_a8a78faf5b3e92f32fe42a94751a74f1=1602073071; prelogid=52d989ba84178ca598460d979c5c2f4b; tal_token=tal173Zz7o1Qekcu2mK2sBrlvVKD7o-pRfW8N5TncB1LhdpQJ68JDnLF5JywtRwX8bXNZcSVoN7h-HQg0gsnSE1k5vFtsTEINeifp3jKtXnA2n1PdLqL7JOJsIR0wvy9fXkg-ufBjDEsE80-6OvF1H5E8OmayLYdL8DaFcihRfKPN0gKQleJIup_rZr6VGgPSGMJALtAYDr7enr8v0rilO2rLO-DODpf-xiYQLq1_4dnlKyiBHNqF3s3mA8CuTml4arSrPf1qRhgAE1Na86bXnRX5OUOmiFi_hl8U8qS6Cjg7d8k4I6; xes_run_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIuY29kZS54dWVlcnNpLmNvbSIsImF1ZCI6Ii5jb2RlLnh1ZWVyc2kuY29tIiwiaWF0IjoxNjAyMDczMDcwLCJuYmYiOjE2MDIwNzMwNzAsImV4cCI6MTYwMjA4NzQ3MCwidXNlcl9pZCI6IjIzMzUwMjM3IiwidWEiOiJNb3ppbGxhXC81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0XC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWVcLzc4LjAuMzkwNC4xMDggU2FmYXJpXC81MzcuMzYiLCJpcCI6IjIyMS4yMTkuMTEzLjEyOCJ9.92zLaZgaJ6qa0np9Ys-YikoQSCV7K71oc-cLhF1mBAc; X-Request-Id=969fcc90b8086d9f6705542bb9b9b1d8',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        self.a = requests.get(self.url, headers=self.headers)
        self.a.encoding = 'gzip'
        self.p = self.a.text
        # self.respon = self.p.encode('ascii').decode('unicode_escape')
        self.response = json.loads(self.p, strict=False)
        # self.response = self.respons.replace('{', ',').replace('}', ',').replace('\"', '').split(',')
        # del self.response[0]
        self.picture_url = self.response['data']['thumbnail']

    def get_name(self):
        return self.response['data']['name']

    def get_description(self):
        if self.response['data']['description'] == '':
            return None
        else:
            return self.response['data']['description']

    def get_likes(self):
        return self.response['data']['likes']

    def get_unlikes(self):
        return self.response['data']['unlikes']

    def get_favorites(self):
        return self.response['data']['favorites']

    def get_adapt_numbers(self):
        return self.response['data']['source_code_views']

    def download_icon(self):
        import os
        os.makedirs('./', exist_ok=True)
        from urllib.request import urlretrieve
        urlretrieve(self.picture_url, './icon.jpg')
        os.system('icon.jpg')
        string = "start explorer " + os.getcwd()
        os.system(string)
        return True

    def get_author_name(self):
        return self.response['data']['username']

    def get_author_id(self):
        return self.response['data']['user_id']

    def get_work_tags(self):
        tags = self.response['data']['tags']
        list_of_tags = tags.split()
        return list_of_tags

    def get_hot(self):
        return self.response['data']['popular_score']

    def get_views(self):
        return self.response['data']['views']

    def get_first_published_time(self):
        return self.response['data']['published_at']

    def get_latest_modified_time(self):
        return self.response['data']['modified_at']

    def get_latest_updated_time(self):
        return self.response['data']['updated_at']

    def get_created_time(self):
        return self.response['data']['created_at']

    def is_hidden_code(self):
        if self.response['data']['hidden_code'] == 2:
            return False
        else:
            return True


class XesUserSpace:
    def __init__(self, user_id):
        self.url_1 = 'https://code.xueersi.com/api/space/index?user_id=' + str(user_id)
        self.url_2 = 'https://code.xueersi.com/api/space/profile?user_id=' + str(user_id)
        self.headers = {
                    'Content-Type': 'application/json',
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/78.0.3904.108 Safari/537.36"}
        self.p_1 = requests.get(self.url_1, headers=self.headers).text
        self.p_2 = requests.get(self.url_2, headers=self.headers).text
        self.response_index = json.loads(self.p_1, strict=False)
        self.response_profile = json.loads(self.p_2, strict=False)
        self.head_url = self.response_profile['data']['avatar_path']

    def download_user_head(self):
        # 类似于分类讨论【捂脸】
        import tkinter
        from tkinter import filedialog
        h = self.head_url[-3] + self.head_url[-2] + self.head_url[-1]
        if h == 'gif':
            root = tkinter.Tk()
            root.geometry("400x300")
            root.title("请勿关掉此窗口")
            ask = tkinter.filedialog.askdirectory(title='请选择图片的保存文件夹') + '\\' + "icon.gif"
            root.withdraw()
            res = requests.get(url=self.head_url).content
            root.destroy()
            with open(ask, "wb") as f:
                f.write(res)
            return "头像下载完成！"
        elif h == 'jpg':
            root = tkinter.Tk()
            root.geometry("400x300")
            root.title("请勿关掉此窗口")
            ask = tkinter.filedialog.askdirectory(title='请选择图片的保存文件夹') + '\\' + "icon.jpg"
            root.withdraw()
            res = requests.get(url=self.head_url).content
            root.destroy()
            with open(ask, "wb") as f:
                f.write(res)
            return "头像下载完成！"
        else:
            root = tkinter.Tk()
            root.geometry("400x300")
            root.title("请勿关掉此窗口")
            ask = tkinter.filedialog.askdirectory(title='请选择图片的保存文件夹') + '\\' + "icon.png"
            root.withdraw()
            res = requests.get(url=self.head_url).content
            root.destroy()
            with open(ask, "wb") as f:
                f.write(res)
            return "头像下载完成！"

    def get_fans_number(self):
        # 这孩子多少粉了？
        return self.response_profile['data']['fans']

    def get_follows_number(self):
        # 这孩子有几个偶像（关注了几个人）？
        return self.response_profile['data']['follows']

    def is_follow(self):
        # 你有没有关注他呢？？？
        if self.response_profile['data']['is_follow'] == 1:
            return True
        else:
            return False

    def get_realname(self):
        # 他真名叫啥？
        return self.response_profile['data']['realname']

    def get_sign(self):
        # 个性签名是什么？
        return self.response_profile['data']['signature']

    def get_number_of_works(self):
        # 他一共有多少作品（加上没发布的）？
        return self.response_index['data']['overview']['works']

    def get_number_of_likes(self):
        # 他的所有作品一共获了多少赞？
        return self.response_index['data']['overview']['likes']

    def get_number_of_views(self):
        # 总浏览量
        return self.response_index['data']['overview']['views']

    def get_adapted_number(self):
        # 被改编多少次？
        return self.response_index['data']['overview']['source_code_views']

    def get_favorites(self):
        # 被收藏多少次？
        return self.response_index['data']['overview']['favorites']

    def get_first_eight_fans(self):
        # 获取他前八个粉丝的姓名和id
        a_list = []
        for i in self.response_index['data']['fans']['data']:
            a_list.append((i['id'], i['realname']))
        return a_list

    def get_first_eight_favourites(self):
        # 获取他前八个收藏的id、name、作者id和作者名
        a_list = []
        for i in self.response_index['data']['favourites']['data']:
            a_list.append((i['id'], i['name'], i['user_id'], i['user_name']))
        return a_list

    def get_representative_work(self):
        # 代表作
        return self.response_index['data']['representative_work']['name']

