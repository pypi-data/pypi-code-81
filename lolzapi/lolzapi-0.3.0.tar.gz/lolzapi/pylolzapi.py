######################
# By BotFather
# lolz.guru/botfather
######################


#modules
import requests

#classes
class get:
    def __init__(self,api):
        self.api = api
    #List of posts in a thread
    def posts(self, thread_id, page_of_post_id="", post_ids="", page="", limit="", order=""):
        response = requests.get(url=f"https://lolz.guru/api/index.php?posts/&thread_id={thread_id}&page_of_post_id={page_of_post_id}&post_ids={post_ids}&page={page}&limit={limit}&order={order}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Return last post
    def last_post(self, thread_id):
        result = self.posts(thread_id)['thread']['links']['last_post']
        response = requests.get(result).json()
        return response
    #Get section threads
    def threads(self, forum_id="", thread_ids="", creator_user_id="", sticky="", thread_prefix_id="", thread_tag_id="", page="", limit="", order="", thread_create_date="", thread_update_date=""):
        response = requests.get(url=f"https://lolz.guru/api/index.php?threads/&forum_id={forum_id}&thread_ids={thread_ids}&creator_user_id={creator_user_id}&sticky={sticky}&thread_prefix_id={thread_prefix_id}&thread_tag_id={thread_tag_id}&page={page}&limit={limit}&order={order}&thread_create_date={thread_create_date}&thread_update_date={thread_update_date}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Find user
    def findUser(self, username="", user_email=""):
        response = requests.get(url=f"https://lolz.guru/api/index.php?users/find&username={username}&user_email={user_email}").json()
        return response
    #Get profile posts
    def profilePosts(self, userid, page="", limit=""):
        response = requests.get(url=f"https://lolz.guru/api/index.php?users/{userid}/timeline&page={page}&limit={limit}").json()
        return response 
    #Get conversations
    def conversations(self, page="", limit=""):
        response = requests.get(url=f"https://lolz.guru/api/index.php?conversations/&page={page}&limit={limit}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response 
    #Detail information of a thread
    def threadInfo(self, page="", limit=""):
        response = requests.get(url=f"https://lolz.guru/api/index.php?threads/2430762",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response 
    #List of messages in a conversation
    def conversation(self, conversation_id, page="", limit="", order="", before="", after=""):
        response = requests.get(url=f"https://lolz.guru/api/index.php?conversation-messages/&conversation_id={conversation_id}&limit={limit}&page={page}&order={order}&before={before}&after={after}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response 
    #List of notifications
    def notifications(self):
        response = requests.get(url=f"https://lolz.guru/api/index.php?notifications",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response 
    #List of all pages in the system
    def pages(self, parent_page_id="", order=""):
        response = requests.get(url=f"https://lolz.guru/api/index.php?pages",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Detail information of a page
    def pagesById(self, page_id):
        response = requests.get(url=f"https://lolz.guru/api/index.php?pages/{page_id}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
class post:
    def __init__(self,api):
        self.api = api
    #Create a new post
    def post(self, thread_id, post_body, quote_post_id=""):
        response = requests.post(url=f"https://lolz.guru/api/index.php?posts/&thread_id={thread_id}&post_body={post_body}&quote_post_id={quote_post_id}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Like post
    def like(self, post_id):
        response = requests.post(url=f"https://lolz.guru/api/index.php?posts/{post_id}/likes",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Profile post
    def profilePost(self, userid, post_body, status=""):
        response = requests.post(url=f"https://lolz.guru/api/index.php?users/{userid}/timeline&post_body={post_body}&status={status}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Sub
    def sub(self, userid):
        response = requests.post(url=f"https://lolz.guru/api/index.php?users/{userid}/followers",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Create a new conversation message
    def conversation(self, conversation_id, message_body):
        response = requests.post(url=f"https://lolz.guru/api/index.php?conversation-messages/&conversation_id={conversation_id}&message_body={message_body}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Like a profile post
    def likeProfilePost(self, post_id):
        response = requests.post(url=f"https://lolz.guru/api/index.php?profile-posts/{post_id}/likes",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
class delete:
    def __init__(self,api):
        self.api = api
    #Unlike post
    def like(self, post_id):
        response = requests.delete(url=f"https://lolz.guru/api/index.php?posts/{post_id}/likes",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Delete post
    def post(self, post_id, reason=""):
        response = requests.delete(url=f"https://lolz.guru/api/index.php?posts/{post_id}&reason={reason}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Delete post
    def thread(self, thread_id, reason=""):
        response = requests.delete(url=f"https://lolz.guru/api/index.php?threads/{thread_id}/&reason={reason}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Delete sub
    def sub(self, userid):
        response = requests.delete(url=f"https://lolz.guru/api/index.php?users/{userid}/followers",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Delete a profile post
    def profilePost(self, post_id, reason=""):
        response = requests.delete(url=f"https://lolz.guru/api/index.php?profile-posts/{post_id}/&reason={reason}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
    #Unlike a profile post
    def likeProfilePost(self, post_id):
        response = requests.delete(url=f"https://lolz.guru/api/index.php?profile-posts/{post_id}/likes",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
class put:
    def __init__(self,api):
        self.api = api
    #Edit message
    def editMessage(self, message_id, message_body):
        response = requests.put(url=f"https://lolz.guru/api/index.php?conversation-messages/{message_id}/&message_body={message_body}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
    #Edit a profile post
    def profilePost(self, post_id, post_body):
        response = requests.put(url=f"https://lolz.guru/api/index.php?profile-posts/{post_id}/&post_body={post_body}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
class api:
    def __init__(self, api):
        self.api = api #set api
        self.get = get(self.api)
        self.post = post(self.api)
        self.delete = delete(self.api)
        self.put = put(self.api)
    def getMe(self):
        response = requests.get(url=f"https://lolz.guru/api/index.php?users/me",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response