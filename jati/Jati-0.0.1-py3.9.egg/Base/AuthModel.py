from Jati.Base.Model import Model

class AuthModel(Model):
    def __init__(self):
        Model.__init__(self)
        self.__authmethod = {
            "login" : None,
        }
    
    def login(self, username, password):
        return None