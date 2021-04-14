from abc import abstractmethod, ABC

class ABCRecommender(ABC):
    
    @abstractmethod
    def getsimilaritems(self, item_name, k):
        pass
    
    @abstractmethod
    def getuserrecommendations(self, user_id):
        pass
    