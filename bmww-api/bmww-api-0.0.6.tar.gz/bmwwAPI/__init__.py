from .users import users
from .work import works

class bmww():
    def __init__(self):
        pass

    def work(self, id=None):
        work = works(id)
        return work


    def users(self, uid):
        user_info = users(str(uid))
        return user_info