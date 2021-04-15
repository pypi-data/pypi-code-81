import requests

class Bwitter():
    def __init__(self):
        self.s = requests.Session()
        self.debug = False
    
    def login(self,uname,pword):
        self.credentials = self.credentials = {"username_or_email":uname,"password":pword, "remember_me":"1"}
        self.loginguy = self.s.post("https://bwitter.me/sessions", data=self.credentials)
    
    def post(self,topost):
        self.postto = {"content":topost}
        self.posted = self.s.post("https://bwitter.me/bweet",data=self.postto)
