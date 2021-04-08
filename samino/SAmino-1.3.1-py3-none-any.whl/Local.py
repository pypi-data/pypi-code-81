from .lib import pack, objects
import requests
import json


class LocalClient:
    def __init__(self, comId: str, sid: str, uid: str):
        self.comId = comId
        self.api = 'https://service.narvii.com/api/v1/'
        self.chat = '/s/chat/thread/'
        self.sid = sid
        self.uid = uid
        self.headers = {
            "NDCDEVICEID": "019B6133991CBC2428F822E55AEF0499B3E674928B3268072CC9381881024F07047DCB9A82899C91B8",
            "NDCAUTH": f'{self.sid}'
        }

    def get_public_chats(self, type: str = 'recommended', start: int = 0, size: int = 25):
        r = requests.get(f'{self.api + self.comId + self.chat}?type=public-all&filterType={type}&start={str(start)}&size={str(size)}',headers=self.headers).text
        request = json.loads(r)
        return objects.ChatThreads(request['threadList']).ChatThreads

    def send_message(self, chatId: str, message: str, type: int = 0, refId: int = pack.timestamp() // 1000):

        data = {
            'content': message,
            'type': type,
            'clientRefId': refId
        }
        data = json.dumps(data)
        r = requests.post(url=f'{self.api + self.comId + self.chat + chatId}/message', data=data, headers=self.headers).text
        request = json.loads(r)
        return objects.ApiMsg(response=request)

    def leave_chat(self, chatId: str):
        r = requests.delete(url=f'{self.api + self.comId + self.chat + chatId}/member/' + self.uid, headers=self.headers).text
        request = json.loads(r)
        return objects.ApiMsg(response=request)

    def join_chat(self, chatId: str):
        r = requests.post(url=f'{self.api + self.comId + self.chat + chatId}/member/' + self.uid, headers=self.headers).text
        request = json.loads(r)
        return objects.ApiMsg(response=request)

    def get_online_members(self, start: int = 0, size: int = 25):
        r = requests.get(f'{self.api + self.comId}/s/live-layer?topic=ndtopic:{self.comId}:online-members&start={str(start)}&size={str(size)}', headers=self.headers).text
        request = json.loads(r)
        return objects.MembersList(request['userProfileList']).MembersList

    def invite_to_chat(self, userId: [str, list], chatId: str):
        data = json.dumps({
            "uids": userId,
        })
        r = requests.post(f"{self.api + self.comId + self.chat + chatId}/member/invite", headers=self.headers, data=data)
        request = json.loads(r.text)
        return objects.ApiMsg(request)

    def voice_invite(self, chatId: str, userId: str):
        data = json.dumps({
            "uid": userId
        })
        r = requests.post(f"{self.api + self.comId + self.chat + chatId}/vvchat-presenter/invite/", headers=self.headers, data=data)
        request = json.loads(r.text)
        return objects.ApiMsg(request)

    # API was Discovered by bovonos
    def invite_by_host(self, chatId: str, userId: [str, list]):
        data = json.dumps({
            "uidList": userId
        })
        r = requests.post(f"{self.api + self.comId + self.chat + chatId}/avchat-members",headers=self.headers, data=data)
        request = json.loads(r.text)
        return objects.ApiMsg(request)

    def start_chat(self, userId: [str, list], message: str, title: str = None, content: str = None, type: int = 0):
        data = json.dumps({
        	"type": type,
            "title": title,
            "inviteeUids": userId,
            "initialMessageContent": message,
            "content": content,
            "timestamp": pack.timestamp()
        })
        r = requests.post(f"{self.api + self.comId + self.chat}", headers=self.headers, data=data)
        request = json.loads(r.text)
        return objects.ApiMsg(request)

    def edit_chat(self, chatId: str, content: str, title: str):
        data = json.dumps({
            "content": content,
            "title": title
        })
        r = requests.post(f"{self.api + self.comId + self.chat + chatId}", headers=self.headers, data=data)
        request = json.loads(r.text)
        return objects.ApiMsg(request)

    def comment(self, comment: str, userId: str = None, blogId: str = None, wikiId: str = None):
        d = {
            "content": comment,
            "stickerId": None,
            "type": 0,
            "timestamp": pack.timestamp()
        }
        if userId:
            d["eventSource"] = "UserProfileView"
            data = json.dumps(d)
            r = requests.post(f"{self.api + self.comId}/s/user-profile/{userId}/comment",headers=self.headers, data=data)

        elif blogId:
            d["eventSource"] = "PostDetailView"
            data = json.dumps(d)
            r = requests.post(f"{self.api + self.comId}/s/blog/{blogId}/comment", headers=self.headers, data=data)

        elif wikiId:
            d["eventSource"] = "PostDetailView"
            data = json.dumps(d)
            r = requests.post(f"{self.api + self.comId}/s/item/{wikiId}/comment", headers=self.headers, data=data)

        request = json.loads(r.text)
        return objects.ApiMsg(request)

    def get_all_users(self, type: str = "recent", start: int = 0, size: int = 25):
        if type == "recent": r = requests.get(f"{self.api + self.comId}/s/user-profile?type=recent&start={start}&size={size}", headers=self.headers)
        elif type == "banned": r = requests.get(f"{self.api + self.comId}/s/user-profile?type=banned&start={start}&size={size}", headers=self.headers)
        elif type == "featured": r = requests.get(f"{self.api + self.comId}/s/user-profile?type=featured&start={start}&size={size}", headers=self.headers)
        elif type == "leaders": r = requests.get(f"{self.api + self.comId}/s/user-profile?type=leaders&start={start}&size={size}", headers=self.headers)
        elif type == "curators": r = requests.get(f"{self.api + self.comId}/s/user-profile?type=curators&start={start}&size={size}", headers=self.headers)
        else: raise TypeError(type)
        request = json.loads(r.text)
        return objects.MembersList(request).MembersList

    def get_user_blogs(self, userId: str, start: int = 0, size: int = 25):
        r = requests.get(f"{self.api + self.comId}/s/blog?type=user&q={userId}&start={start}&size={size}", headers=self.headers)
        request = json.loads(r.text)
        return objects.BlogList(request['blogList']).BlogList

    def get_user_wikis(self, userId: str, start: int = 0, size: int = 25):
        r = requests.get(f"{self.api + self.comId}/s/item?type=user-all&start={start}&size={size}&cv=1.2&uid={userId}", headers=self.headers)
        request = json.loads(r.text)
        return objects.WikiList(request['itemList']).WikiList

    def get_wall_comments(self, userId: str, sort: str = "newest", start: int = 0, size: int = 25):
        if sort == "newest": sort = "newest"
        elif sort == "oldest": sort = "oldest"
        elif sort == "top": sort = "vote"
        else: raise TypeError(sort)
        r = requests.get(f"{self.api + self.comId}/s/user-profile/{userId}/comment?sort={sort}&start={start}&size={size}", headers=self.headers)
        request = json.loads(r.text)
        return objects.CommentList(request["commentList"]).CommentList

    def like_blog(self, blogId: str = None, wikiId: str = None):
        d = {
            "value": 4,
        }
        if blogId:
            d["eventSource"] = "UserProfileView"
            data = json.dumps(d)
            r = requests.post(f"{self.api + self.comId}/s/blog/{blogId}/vote?cv=1.2", headers=self.headers, data=data)
        elif wikiId:
            d["eventSource"] = "PostDetailView"
            data = json.dumps(d)
            r = requests.post(f"{self.api + self.comId}/s/item/{wikiId}/vote?cv=1.2", headers=self.headers, data=data)
        request = json.loads(r.text)
        return objects.ApiMsg(request)

    def like_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None):
        d = {
            "value": 1,
        }
        if userId:
            d["eventSource"] = "UserProfileView"
            data = json.dumps(d)
            r = requests.post(f"{self.api + self.comId}/s/user-profile/{userId}/comment/{commentId}/vote?cv=1.2&value=1", headers=self.headers, data=data)

        elif blogId:
            d["eventSource"] = "PostDetailView"
            data = json.dumps(d)
            r = requests.post(f"{self.api + self.comId}/s/blog/{blogId}/comment/{commentId}/vote?cv=1.2&value=1", headers=self.headers, data=data)
        elif wikiId:
            d["eventSource"] = "PostDetailView"
            data = json.dumps(d)
            r = requests.post(f"{self.api + self.comId}/s/item/{wikiId}/comment/{commentId}/g-vote?cv=1.2&value=1", headers=self.headers, data=data)
        request = json.loads(r.text)
        return objects.ApiMsg(request)
