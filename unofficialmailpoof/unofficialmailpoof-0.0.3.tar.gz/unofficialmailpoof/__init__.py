from time import sleep
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class MailpoofBot:
    def __init__(self, email):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1280, 800)
        if not re.match(email, 'mailpoof'):
            email = email + '@mailpoof.com'
        self.driver.get("https://mailpoof.com/mailbox/" + email)
        sleep(10)

    def getmails(self):
        mails = self.driver.find_elements_by_class_name('mail-item')
        mailarray = []

        for m in mails:
            self.driver.find_element_by_id(m.get_attribute("id")).click()
            sleep(1)
            mailelement = self.driver.find_element_by_id("content-" + m.get_attribute("id"))
            linkelements = self.driver.find_elements_by_tag_name("a")
            links = []
            meta = mailelement.text.split('\n', 3)
            x = re.findall("\S+@\S{3,}", meta[1])
            text = mailelement.text

            for link in linkelements:
                if re.search("^((?!mailpoof).)*$", link.get_attribute("href")) is not None:
                    links.append(link.get_attribute("href"))

            mail = [meta[0], x[0], meta[2], text, links]
            mailarray.append(mail)

        return mailarray


def getallmails(email):
    mp = MailpoofBot(email)
    mails = mp.getmails()
    return mails
