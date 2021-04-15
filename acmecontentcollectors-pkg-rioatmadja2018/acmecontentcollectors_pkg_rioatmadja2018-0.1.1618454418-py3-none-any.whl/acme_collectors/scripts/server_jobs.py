#!/usr/bin/env python
from acme_collectors.collectors.contents_collector import ContentsCollector
from acme_collectors.utils.constants import TOPICS 
from typing import List, Dict 
import multiprocessing as mp
import time
import pandas as pd
from base64 import urlsafe_b64encode
from acme_collectors.engines.mysql_engine import MySQLEngine
from acme_collectors.engines.notifications import Notifications
from acme_collectors.utils.constants import CREATE_TABLE
from datetime import datetime
import numpy as np 
np.random.seed(10000) 

"""
yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyssssssssssssssyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyssoo+++/+++++++++++++++++oosssyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyyyyyyyyyyyyyyysoo+/++ooooooooooo+++++++++ooooooooooossyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyyyyyyyyyyysoo+++oooo+++++++++o+++o+oooooo++oo++++ooooo+ossyyyyyyyyyyyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyyyyyyyyso+++ooo++++/ooss++ooooo+++o+osoo+osoososo+oo++ooo+oosyyyyyyyyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyyyyyso++ooo++++oooooooso+ooooooo+ooooos++++o+soso+o+sooo++oo++osyyyyyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyyss+++ooo++/+oooo++o+osoosososssssssoss+/+ooso+++oosooos++ooooo+osyyyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyss++ooo++oossosoo+o+osss++++++////////+////++++/oooso+ss++oosoo+oo++syyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyoo+ooo+ooos+++ooooss++++++////////////////:///////++oosso+++oysssoooo++oyyyyyyyyyyyyyy
yyyyyyyyyyyyso+ooo+++oosoo++oss++///+///////::://////://::+/////+/+++o+ooossoooo+++oo++syyyyyyyyyyyy
yyyyyyyyyyso++oo++++++++ossso++++///////////////////////:///////+++/++++osso++++++++ooo+osyyyyyyyyyy
yyyyyyyyyso+ooo++++++++++o++++++//+///+///:///////////////:////+++++++++++o+++++++++++oo++syyyyyyyyy
yyyyyyyyo++oo++++++++++++++++++/+++////////////+///////////+//+++++++++++++++++++++oo+++oo+oyyyyyyyy
yyyyyyyo++so+++++++++++++++++++++///++++//++/++/+++///+++/++++++++++++++++++++++++++++oo+oo+oyyyyyyy
yyyyyyo++so++++++++++++++++++++++/+//+++++/+++++++///+/+++++++++++++++++++++++++++oo+oo+oooo+oyyyyyy
yyyyyo++so+++++++++++++++++++++++++++++++++++++++++++++++/+++++++++++++++++++++++ooo++o+ooooo+oyyyyy
yyyys++oo++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++oooooooo++syyyy
yyyy++ooo++++++++ooo+++//+++++++++++++++++++++++++++/+/++++++++++++++++++++++++ooos++ooooooooo++syyy
yyyo++soo++++++++ossysso++++++/++++++++++++++++++++++++++++/++++++++////++++ossysysoooooooooooo+oyyy
yyso+oo+++++++++++++oossssso+++//++++++++++++++++++++++++++/+////////++oosysysooooooooo+ooooooo++syy
yyo++oo+++++o++oo++++++++oosssoo++/++++++++/+++++++++++//////+++++++oosyssoooo+oooo+o+oooooooooo+oyy
yyo+ooooo+++++oo++++++++++++++oosooooo++/+//++++++//////+++++ooossssoo+++++++o+o+o++oooooooooooo++yy
yso+so+++++oooo+++++++++++++++++++++sssooo+++//+++++++++++ossssso++++++++++++++ooooooooooooooooo++sy
yso+ooo+++++o+oooo++++++++++++++oo+oo++++oooooo++oo+//++oooo++++o+os++++++o+++oooooooooooooooooo++sy
yy++ooooooooooooo+oo+++++++++++ohoo++oooo+so++osssso++++soo+o+soossdo+++++++++o+oooo+oooooooooo+++sy
yy++oo+++++++ooo++o+ooooo+++++++syssosssoyyssso++++oossoyo+oosyoossso+++o+o+o+ooooo+oo++oooooooo++yy
yy++oo+o+++ooooooooooo++++++++++hhyyyssssoo+++++++++++++oossso++++++o++++++++oooooo+oooossoo++oo++yy
ys++oooyyssssoooooooo++++++so+++osysyyo++++++++++++++++++++++od+y+++++oo++o+ooo+oooooo+oysooooso++yy
yso+oosssssssoooo+o+++//+oso++osyyyhyo++++++++++++++++++++++++yyyhyoo++oys+++++ooooooooosyyysyso+oyy
yyo+oooooooossooo++++++oso+ossoooooo+++++++++++++++++++++++++oooooooosoo+oss++++ooooo+ossoooosoo+syy
yys++oossssoosoos+++++++oshsoooo++++++++++++++++o++++++o+++oo+++oooooooshsooso++++yooososssooso++syy
yyyo+oossssssssooo++++ossoooo+oooooooooo+o+++o+o+oo+++oo+ooooooooooooooosyssoo+++oyooosssssysso+oyyy
yyys++oosssyyysooososssoooooooo+oooooooooo++oo++oooooooooooooooooooooooooooooysooyooooossssyso++syyy
yyyyo+oossooooosooosooooooooooooooooooooooooooooooooooooooooooooooooooooooooooosyooosssysysso++oyyyy
yyyyso+oosoossyssooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo+osoooooyso+osyyyy
yyyyyso+oosyssossoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooosssssssso++syyyyy
yyyyyyso+oosooossssoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooosysssssyso++syyyyyy
yyyyyyyso+oosoosysssso+ooooooooooooooooooooooooooooooooooooooooooooooooooooooo+ooooossssso+osyyyyyyy
yyyyyyyyso+oosssoosssooooooooooooooooooooooooooooooooooooooooooooooooooooooooosssssoosys++osyyyyyyyy
yyyyyyyyyso++osoooossssssooooooooooooooooooooooooooooooooooooooooooooooooooooosysysssso++ssyyyyyyyyy
yyyyyyyyyyyso+oossssysssssooooooooooooooooooooooooooooooooooooooooooooo+ooooooosyssss++osyyyyyyyyyyy
yyyyyyyyyyyyso++oosssssooosssoooooooooooooooooooooooooooooooooooooooooosssooooooyyso+osyyyyyyyyyyyyy
yyyyyyyyyyyyyyso++oosssoosyososooooooooooooooooooooooooooooooooo++ooossoosssooooo+++osyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyso++oossosoossyooooooooooo+oooooooooooo++++ooooossssossssssssoo+++osyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyyyso+++ossssssooooossossoooo+oosoooosooosossssyssssososssysso++ossyyyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyyyyysoo+++ooooooosossossossssysyossssssysyssssossyssysoooo+++osyyyyyyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyyyyyyyysoo++++ooosssosysoosoysooosyyosoooyoyooosysssso++++ossyyyyyyyyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyyyyyyyyyyyssso++++oossooosysssossyssysssoyssssooo+++++osssyyyyyyyyyyyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyssoo+++++++ooooossssossoooo+++++++oossyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyysssssooo++++++++++++ooooosssyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

Name: Rio Atmadja
Description: Helper scripts to collect data and store them inside MySQL database 
Date: November 25, 2020 

Search Keywords:
    Description: Keywords associations with the Islamic State (Daesh) 

    - 
"""

acme_content = ContentsCollector()

# Cycle different topic on each run 
key_words: List[str] = list(TOPICS)
np.random.shuffle(key_words)
number_of_topic: int = np.random.randint(1,len(key_words) - 1)
SEARCH_KEYWORDS: Dict = dict(map(lambda key_word: (key_word, TOPICS.get(key_word)), key_words[0:number_of_topic]))

# Do Google Search
google_query_results: List = []
list_of_topics: List = []

for word, keyword in SEARCH_KEYWORDS.items():
    print(f"[\033[32mDONE\033[0m] SEARCHING FOR KEYWORD: {word.replace('_', ' ').title()}")
    urls: List[str] = acme_content.search_contents_from_google(keyword=keyword)
    google_query_results.extend(urls)
    list_of_topics.extend([word] * len(urls))

print(f"\n[\033[32mDONE\033[0m] Creating CPU pool for Mining Tasks.")

# Grab the contents from https://justpaste.it
justpasteit_results: List = []
pools = mp.Pool(mp.cpu_count())

start_time: float = time.time()
for topic, url in zip(list_of_topics,google_query_results):
    try:
        print(f"[ \033[32mDONE\033[0m ] Parsing content from {url}")
        justpasteit_results.append(pools.apply_async(acme_content.justpasteit_contents, (url,topic,)).get(timeout=60))
    except:
        print(f"[\033[31mFAILED\033[0m] Failed parsing content from {url}")
        pass
pools.close()
pools.join()

print(justpasteit_results)

# Encode posts and image url to base64
df = pd.DataFrame(justpasteit_results)
df['posts'] = df['posts'].astype(str).apply(lambda post: urlsafe_b64encode(post.encode('utf-8')))
df['image_url'] = df['image_url'].astype(str).apply(lambda image_url: urlsafe_b64encode(image_url.encode('utf-8')))
df['number_views'] = df['number_views'].astype(str).apply(lambda view: urlsafe_b64encode(view.encode('utf-8')))

df = df.drop_duplicates(subset='posts') # remove duplicate posts 

mysql_engine = MySQLEngine(host='127.0.0.1', user='cloud_user')
# Create MySQL table to store data, otherwise skip it
try:
    mysql_engine.create_table(create_tbl_query=CREATE_TABLE, table_name='justpasteit_posts')
except:
    pass

# Create arguments and insert query
args: List[tuple] = list(map(lambda column: tuple(column), df.values.tolist()))
insert_query: str =  "INSERT INTO justpasteit_posts(%s) VALUES (%s)" % (', '.join(df.columns.tolist()), ', '.join(['%s'] * df.shape[1] ))

# Insert data into MySQL Table
mysql_engine.bulk_insert(insert_query=insert_query, args=args)

# Send the notification to the admin
notify = Notifications()
email_address: str = "rioatmadja2018@gmail.com"
email_subject: str = datetime.utcnow().strftime('%Y-%m-%d @%H:%M:%S')
current_topics: List[str] = list(map(lambda topic: topic.replace("_", " ").title(), key_words[0:number_of_topic])) # convert the given string to title 
notification_msg: str = f"Friendly reminder your topics {' , '.join(current_topics)} have been processed."
print(f"[\033[32m+\033[0m] Sending notification to {email_address}")
notify.send_notification(email_address=email_address, notification_subject=email_subject, notification_msg=notification_msg)
print(f"[\033[32m+\033[0m] Time Elapsed: {time.time() - start_time} ")
