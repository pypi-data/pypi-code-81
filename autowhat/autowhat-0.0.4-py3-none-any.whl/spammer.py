from time import sleep
from selenium import webdriver
from autowhat.helper import chat_selector, message_writer


def spam_bot(name: str, msg: str, count: int, driver: webdriver):
    chat_selector(name, driver)
    for i in range(count):
        select = True
        message_writer(msg, select=select, driver=driver)
    sleep(1)
