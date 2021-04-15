#!/usr/bin/env python
from acme_collectors.utils.constants import HEADERS
import re
from phantomjs import Phantom
from typing import Dict, List
from bs4 import BeautifulSoup

class CNNENGINE(object):
    """
    DESCRIPTION
    -----------
    Helper class to parse the contents from the CNN class

    PARAMETERS
    ----------
    :topic: given a non-empty and valid topic
    :size: an optional parameters with a default search size of 10

    EXAMPLE
    -------
    >>>
    >>>
    """
    def __init__(self, topic: str =  "" , size: int = 10, category: str = ""):

        self.query: str = "" 
        self.config: Dict = {'headers': HEADERS}

        if topic:
            self.encoded_puncts: Dict = {char: hex(ord(char)).replace('0x', '%') for char in re.findall(r'\W', topic)}
            self.topic: str = ''.join([self.encoded_puncts.get(char, char) for char in topic])
            self.query = f"https://www.cnn.com/search?size={size}&q={self.topic.lower()}"

            if category:
                self.query = self.query + f"&category={category}"

            self.config['url'] = self.query 

    def cnn_browser(self) -> str:
        """
        Description
        -----------
        Helper method to make query to the CNN Website

        Parameters
        ----------
        :config: an optional dictionary parameter

        Returns
        -------
        :return: a string of response
        """
        if not self.config:
            raise AttributeError("Please provide a valid URL or kwargs configurations.")

        try:

            phantom_browser = Phantom()
            response: str = phantom_browser.download_page(conf=self.config)
            return response

        except ConnectionError as e:
            raise ConnectionError(f"[ERROR] Unable to connect to the following url: {self.query}") from e

    def get_categories(self) -> List[str]:
        """
        Description
        -----------
        Helper method to display different types of CNN categories

        Returns
        -------
        :return: a list with the category attributes
        """

        return ['us', 'world', 'politics', 'business', 'opinion', 'health', 'entertainment', 'style', 'travel']

    def get_cnn_links(self, url: str = "") -> tuple:
        """
        Description
        -----------
        Helper method to extract all the CNN's links

        Parameters
        ----------
        :url: an optional url parameter

        Returns
        -------
        :return: a list of strings that contain CNN links
        """
        
        if url:
            if 'www.cnn.com' not in url: 
                raise AttributeError(f"Please provide the right CNN URLs")

            self.config['url'] =  url
 
        cnn_response: str = self.cnn_browser()

        soup = BeautifulSoup(cnn_response.encode('utf-8'))
        cnn_links: [str] = list(set([f"https:{a.get('href')}" for a in soup.find_all('a') if re.findall(r"www.cnn.com.*.html", a.get('href')) and 'sitemap.html' not in a.get('href')]))
        next_page: List[str] = self.next_page(soup=soup)

        return (cnn_links, next_page)

    def parse_content(self, url: str) -> str:
        """
        Description
        -----------
        Helper method to parse the individual CNN page

        Parameters
        ----------
        :url: given a valid cnn link

        Returns
        -------
        :return: a string with the CNN contents
        """

        if not url and 'www.cnn.com' not in url: 
            raise AttributeError("Please provide a valid cnn url.")

        self.config['url'] =  url
        cnn_response: str = self.cnn_browser()
        soup = BeautifulSoup(cnn_response.encode('utf-8'))

        return ' '.join([x.text for x in soup.find_all('div') if 'l-container' in x.get('class', '')])

    def traverse_page(self, depth: int = 30) -> List:
        """
        Description
        -----------
        Helper function to traverse the CNN links by the given depth

        Parameters
        ----------
        :depth: an optional depth parameter with default of 30

        Returns
        -------
        :return: a list of the CNN articles
        """

        cnn_articles: List = []
        for page in range(0, depth, 10):
            url: str = f"{self.query}&from={page}&page={round(page/10) + 1}"
            cnn_links, next_page = self.get_cnn_links(url=url)

            if not next_page:
                return cnn_articles

            for link in cnn_links:
                link = re.sub(r"", "", link)
                cnn_articles.append(self.parse_content(url=link))

        return list(set(cnn_articles))  # return unique news articles 

    def next_page(self, soup: BeautifulSoup) -> List:
        """
        Description
        -----------
        Helper method to index the next page

        Parameters
        ----------
        :soup: a beautiful soup object

        Returns
        -------
        :return: a list of string that contains the page numbers
        """
        if not isinstance(soup, BeautifulSoup):
            raise TypeError("Please provide a beautiful soup object.")

        return [x.text for x in soup.find_all('span') if 'SearchPageLink' in ' '.join(x.get('class', []))]

