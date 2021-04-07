class Category(object):

    def __init__(self,jsonresponse):
        self.__code = jsonresponse['code']
        self.__label = jsonresponse['label']
        self.__number_of_mentions = jsonresponse['numberOfMentions']
        self.__sub_categories = {}
        sub_categories = jsonresponse['subCategories']
        for s in sub_categories:
            self.__sub_categories.append(Category(s))

    def getCode(self):
        '''
        Code of the category.
        :returns: 
        '''
        return self.__code

    def getLabel(self):
        '''
        Label of the category
        :returns: 
        '''
        return self.__label

    def getNumberOfMentions(self):
        '''
        Number of mentions in the category.
        :returns: 
        '''
        return self.__number_of_mentions

    def getSubCategories(self):
        '''
        All the sub categories of the category.
        :returns: 
        '''
        return self.__sub_categories