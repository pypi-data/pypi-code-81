#!/usr/bin/env python
from acme_collectors.utils.helpers import get_current_credential_paths
from typing import Dict, List 
"""
Name: Rio Atmadja
Date: November 25, 2020
Description: Constant script
"""

# Create justpasteit_posts 
CREATE_TABLE: str = """
    CREATE TABLE `justpasteit_posts` (
        `post_id` INT(11) NOT NULL AUTO_INCREMENT, 
        `date_created` TEXT, 
        `post_modified` TEXT, 
        `number_views` VARCHAR(255), 
        `url` VARCHAR(255),
        `search_keyword` TEXT,  
        `image_url` TEXT, 
        `language` VARCHAR(255), 
        `posts` LONGTEXT , 
        PRIMARY KEY (post_id) 
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

# Notification template
NOTIFICATION_TEMPLATE: str = """
To: %s
From: dscnotifier@gmail.com  
Subject: %s

NOTIFICATION 
--------------------------------
Server Name: %s
Server Address: %s
LOG Reference: %s
--------------------------------

MESSAGE
--------------------------------
%s
"""

# Create translated_posts 
TRANSLATED_TBL: str = """
    CREATE TABLE `translated_posts` (
        `translated_id` INT(11) NOT NULL AUTO_INCREMENT,
        `post_id` INT(11),
        `image_id` INT(11),
        `post_url` TEXT,
        `image_url` TEXT,
        `language` VARCHAR(255),
        `posts_md5` VARCHAR(255), 
        `translated` BOOLEAN, 
        PRIMARY KEY (translated_id) 
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8; 
"""
# Query to store images
IMAGE_URLS: str = """
    CREATE TABLE `image_urls_justpasteit` (
        `image_id` INT(11) NOT NULL AUTO_INCREMENT , 
        `post_url` VARCHAR(255), 
        `image_url` TEXT , 
        `embedded_text` LONGTEXT,
        `translated_text` LONGTEXT, 
        `language` VARCHAR(255), 
        `translated` BOOLEAN, 
        PRIMARY KEY (image_id) 
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

# NOTE: Current topics for now, add more later
TOPICS: Dict = {
    'islamic_state': '%D8%A7%D9%84%D8%AF%D9%88%D9%84%D8%A9%20%D8%A7%D9%84%D8%A5%D8%B3%D9%84%D8%A7%D9%85%D9%8A%D8%A9',
    'daesh': '%D8%AF%D8%A7%D8%B9%D8%B4',
    'dogs_of_fire': '%D9%83%D9%84%D8%A7%D8%A8%20%D8%A7%D9%84%D9%86%D8%A7%D8%B1', # dogs of fire (term for a suicide bomber)
    'dogs_of_baghdadi': '%D9%83%D9%84%D8%A7%D8%A8%20%D8%A7%D9%84%D8%A8%D8%BA%D8%AF%D8%A7%D8%AF%D9%8A',
    'in_the_shadow_of_caliphate': '%D9%81%D9%8A%20%D8%B8%D9%84%20%D8%A7%D9%84%D8%AE%D9%84%D8%A7%D9%81%D8%A9', # word association with the crime/action commited by the daesh
    'mujahideen': '%D8%A7%D9%84%D9%85%D8%AC%D8%A7%D9%87%D8%AF%D9%88%D9%86',
    'lions_of_the_islamic_state': '%D8%A3%D8%B3%D9%88%D8%AF%20%D8%A7%D9%84%D8%AF%D9%88%D9%84%D8%A9%20%D8%A7%D9%84%D8%A5%D8%B3%D9%84%D8%A7%D9%85%D9%8A%D8%A9',
    'soldiers_of_the_caliphate': '%D8%AC%D9%86%D9%88%D8%AF%20%D8%A7%D9%84%D8%AE%D9%84%D8%A7%D9%81%D8%A9',
    'caliph': '%D8%A7%D9%84%D8%AE%D9%84%D8%A7%D9%81%D8%A9%20'

}

PKL_CLF: str = "./acme_collectors/utils/tools/random_forest.gz"
TONES: List[str] = ['Analytical', 'Joy', 'Sadness', 'Fear', 'Confident', 'Anger', 'Tentative'] 
HEADERS: Dict = {'Accept': '*/*',
                  'Accept-Language': 'en-US,en;q=0.5', 
                  'Encoding': 'gzip, deflate, br', 
                  'User-Agent': 'Mozilla/5.0 (ACME Content Collector; Linux x86_64; x64; rv:84.0) Gecko/20000101 Firefox/34.0'
                }
# NOTE: Location to your credentials
CREDENTIAL_PATH: str = get_current_credential_paths()
