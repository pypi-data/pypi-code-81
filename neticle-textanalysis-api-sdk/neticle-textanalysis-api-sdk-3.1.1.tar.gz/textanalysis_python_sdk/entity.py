

class Entity(object):

    def __init__(self, jsonresponse):
        self.__uuid = jsonresponse['uuid']
        self.__mention_number = jsonresponse['mentionNumber']
        self.__opinion_index = jsonresponse['opinionIndex']
        self.__name = jsonresponse['name']
        self.__type = jsonresponse['type']
        self.__sentences = jsonresponse['sentences']

    def getUUID(self):
        '''
        A unique identifier for this entity.
        :returns: 
        '''
        return self.__uuid

    def getMentionNumber(self):
        '''
        The number of times this entity was found in the input text.
        :returns: An integer value of the number of mentions for this entity.
        '''
        return self.__mention_number

    def getOpinionIndex(self):
        '''
        The overall opinion index of this entity.
        :returns: The overall opinion index of this entity.
        '''
        return self.__opinion_index

    def getName(self):
        '''
        The name of this entity.
        :returns: The name of this entity.
        '''
        return self.__name

    def getType(self):
        '''
        The type of this entity.
        :returns: The type of this entity.
        '''
        return self.__type

    def getSentences(self):
        '''
        The list of the sentence parts' UUIDs in which this entity was found.
        :returns: The list of the sentence parts' UUIDs in which this entity was found.
        '''
        return self.__sentences
