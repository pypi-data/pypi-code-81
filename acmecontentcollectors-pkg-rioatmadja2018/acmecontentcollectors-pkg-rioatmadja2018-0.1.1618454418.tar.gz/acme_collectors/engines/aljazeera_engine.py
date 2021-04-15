#!/usr/bin/env python
from bs4 import BeautifulSoup 
from typing import Dict, List 
from urllib import request 
import re 

class AljazeeraEngine(object):
    """
    DESCRIPTION
    ------------
    Helper class responsible to retrieve contents from the Aljazeera website about a given topic. 

    PARAMETERS
    ----------
    :topic: given a valid topic 

    ATTRIBUTES
    -----------

    EXAMPLES
    --------- 
    ----
    """ 
    def __init__(self, topic: str = ''):
        if not topic: 
            raise ValueError("You must provide a valid topic.\n For example, AljazeeraEngine(topic='Islamic State')")

        self.topic: str = topic 
        self.headers: Dict = {'Accept': '*/*',
                            'Accept-Language': 'en-US,en;q=0.5', 
                            'Encoding': 'gzip, deflate, br', 
                            'User-Agent': 'Mozilla/5.0 (ACME Content Collector; Linux x86_64; x64; rv:84.0) Gecko/20000101 Firefox/34.0'
                            }


    def get_url(self) -> List[str]: 
        """
        Description
        -----------
        Helper funciton to generate query URLs 

        Return
        -------
        :return: a list of string with the aljazeera search query parameters 
        """
        non_alnum: List[str] = re.findall(r'\W',self.topic)
        encode_non_ascii: str = { char:hex(ord(char)).replace('0x', '%') for char in non_alnum} # encode non alpha numeric character 

        for key,value in encode_non_ascii.items(): 
            self.topic = self.topic.replace(key, value)

        return [ f"https://www.aljazeera.com/search/{self.topic}/page={page}" for page in range(1,10) ] 

    def aljazeera_browser(self, url: str) -> bytes: 
        """
        Description
        -----------
        A default browser to parse the Aljazeera contents 

        Parameters
        ----------
        :url: a required url parameter

        Return
        ------
        :return: a response from the Aljazeera website in bytes form 
        """
        if not url:
            raise ValueError(f"Please provide the right url. Please reffer to get_url method.")

        try: 
            return request.urlopen(request.Request(url=url,headers=self.headers)).read() 

        except ConnectionError as e: 
            raise ConnectionError(f"Error: Unable to parse the content from the given url {url}. Please check your query.") from e 

    def get_news_links(self) -> List[str]:
        """
        Description
        -----------
        Helper functions to get the valid Aljazeera news article links 

        Return
        -------
        :return: a list of Aljazeera links 
        """  
        aljazeera_links: List[str] = self.get_url()
        aljazeera_valid_links: List = []
        aljazeera_responses: List = []

        for url in aljazeera_links: 
            aljazeera_responses.append(self.aljazeera_browser(url=url)) 

        # extract the valid Aljazeera links 
        for response in aljazeera_responses:
            try: 
                # filter only Aljazeera links that contain unique article links 
                aljazeera_valid_links.extend(list(set([ tag.get('href') for tag in BeautifulSoup(response).find_all('a') if re.findall(r"/opinions/|/features/|/news/|/tag/", tag.get('href')) and 'www.aljazeera.com' in tag.get('href') ])))

            except: 
                raise Warning(f"Please check the following payload {response}")

        return  list(set(aljazeera_valid_links)) # make sure there is no duplicate links 

    def parse_contents(self) -> Dict:

        # parse the contents from Aljazeera
        article_links: List[str] = self.get_news_links()
        responses: Dict = {}
        for url in article_links: 
            current_page: bytes = self.aljazeera_browser(url=url)
            article_title: str = BeautifulSoup(current_page).find('h1').text.title() 
            responses[article_title] = '\n'.join([ p_tag.text for p_tag in BeautifulSoup(current_page).find_all('p') ]) 

        return responses
                
