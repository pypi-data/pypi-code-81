#!/usr/bin/env python
import pymysql
import pandas as pd
import json

# Exceptions
from json.decoder import JSONDecodeError
from pymysql.err import ProgrammingError, MySQLError

# Alias
from typing import Dict, List
from pandas.core.frame import DataFrame

class ACMEDB(object):
    """
    DESCRIPTION
        Helper class to interact with the ACME database

    FUNCTIONS
        __init__
        __load_credentials__
        __close__
        __bulk_insert
        __get_query
        insert_image_links
        insert_news_contents
        insert_middle_east_regions_attributes
        insert_video_links
        insert_ngrams
        get_news_articles
        get_video_links
        get_image_links
        get_ngrams
    """
    def __init__(self, credentials: str = ""):

        if not credentials:
            raise FileNotFoundError("Please provide the right credential.")

        self.credentials: Dict = self.__load_credentials__(credentials=credentials)
        self.mysql_user: str = self.credentials.get('MYSQL_USER')
        self.mysql_passwd: str = self.credentials.get('MYSQL_PASSWD')
        self.mysql_db: str = self.credentials.get("MYSQL_DB")
        self.mysql_host: str = self.credentials.get("MYSQL_SERVER")
        self.mysql_conn = pymysql.connect(host=self.mysql_host,
                                          user=self.mysql_user,
                                          passwd=self.mysql_passwd,
                                          db=self.mysql_db)
        self.mysql_cursor = self.mysql_conn.cursor()

    def __load_credentials__(self, credentials) -> Dict:

        try:
            return json.loads(open(credentials, 'r').read())

        except JSONDecodeError as e:
            raise JSONDecodeError(f"Unable to load the following credential file {self.credentials}")

    def __close__(self):
        self.mysql_conn.close()

    def __bulk_insert(self, query, items):

        if not all([query, items]):
            raise ValueError("Please provide the right query and items.")

        self.mysql_cursor.executemany(query, items)
        self.mysql_conn.commit()

    def __get_query(self, sql_query: str) -> DataFrame:
        try:
            return pd.read_sql_query(sql_query, con=self.mysql_conn)

        except MySQLError as e:
            raise MySQLError(f"ERROR: Unable to execute the following {sql_query} SQL Statement") from e

    def insert_image_links(self, news_image_links: List[tuple]):
        if not news_image_links:
            raise ValueError("Please insert a valid image links.")

        insert_news_image_links: str = """
            INSERT INTO image_links(region_name, image_urls, image_category, news_url)
                    VALUES (%s,%s,%s,%s)
        """
        self.__bulk_insert(query=insert_news_image_links, items=news_image_links)

    def insert_news_contents(self, news_contents: List[tuple]):
        if not news_contents:
            raise ValueError("Please insert the news contents.")

        insert_news_contents: str = """
            INSERT INTO news_contents(region_name, news_urls, news_category, content)
                    VALUES (%s,%s,%s,%s)
        """
        self.__bulk_insert(query=insert_news_contents, items=news_contents)

    def insert_middle_east_regions_attributes(self, region_attributes: List[tuple]):
        if not region_attributes:
            raise ValueError("Please insert the right region attributes.")

        insert_region_attributes: str = """
            INSERT INTO middle_east_regions(region_name, url, news_date, category, title) VALUES (%s, %s, %s, %s, %s) 
            """
        self.__bulk_insert(query=insert_region_attributes, items=region_attributes)

    def insert_video_links(self, video_links: List[tuple]):
        if not video_links:
            raise ValueError("Please insert the right video links.")

        insert_video_links: str = """
            INSERT INTO video_links(region_name, video_url, video_category, news_url) 
            VALUES (%s, %s, %s, %s) 
            """
        self.__bulk_insert(query=insert_video_links, items=video_links)

    def insert_ngrams(self, ngrams_attributes: List[tuple]):
        if not ngrams_attributes:
            raise ValueError("Please insert the right ngram attributes.")

        insert_ngrams_attributes: str = """
            INSERT INTO ngrams(region_name, news_category, pickle_path) 
            VALUES (%s, %s, %s) 
            """
        self.__bulk_insert(query=insert_ngrams_attributes, items=ngrams_attributes)

    def get_news_articles(self) -> DataFrame:

        # TODO: append the video links
        news_articles_query: str = """
        SELECT 
            mer.region_name,
            mer.url,
            mer.news_date, 
            mer.category, 
            mer.title, 
            nc.content,
            il.image_urls
            
        FROM middle_east_regions mer 
        LEFT JOIN news_contents nc ON nc.news_urls = mer.url AND nc.region_name = mer.region_name 
        LEFT JOIN image_links il ON il.news_url = mer.url AND il.region_name = mer.region_name 
        """
        return self.__get_query(sql_query=news_articles_query)

    def get_video_links(self) -> DataFrame:

        video_links_query: str = """
        SELECT 
            video_id, 
            region_name,
            video_url,
            video_category,
            news_url
        FROM video_links
        """
        return self.__get_query(sql_query=video_links_query)

    def get_image_links(self) -> DataFrame:

        image_links_query: str = """
        SELECT 
            image_id, 
            region_name,
            image_urls,
            image_category,
            news_url
        FROM image_links
        """
        return self.__get_query(sql_query=image_links_query)

    def get_ngrams(self) -> DataFrame:
        search_query: str = """
        SELECT 
            id,
            region_name,
            news_category,
            pickle_path
        FROM ngrams    
        """
        return self.__get_query(sql_query=search_query)
