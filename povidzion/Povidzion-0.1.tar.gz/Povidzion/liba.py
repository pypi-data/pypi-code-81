

class get:
    def __init__(self,username, state):
        self.name = username
        self.state = state
    def Name(self):
        return self.name

    
class User:
    def __init__(self,username, state):
        self.name = username
        self.state = state
        self.get = get(self.name,self.state)
    def print(self):
        print(f"User {self.name} is {self.state}")


        
def hello():
    print("I LOVE MINECRAFT!")

a = 10
b = "V"

if __name__=='__main__':
    print("AAAA")
    print("X3")
