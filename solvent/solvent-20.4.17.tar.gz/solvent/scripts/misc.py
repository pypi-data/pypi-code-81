import random

import pomace

from . import Script


class Salesflare(Script):

    URL = "https://integrations.salesflare.com/s/tortii"
    SKIP = True

    def run(self, page) -> pomace.Page:
        pomace.log.info("Launching form")
        page = page.click_request_this_listing(wait=0)
        page.fill_email(pomace.fake.email)
        page.fill_company(pomace.fake.company)

        pomace.log.info("Submitting form")
        return page.click_submit(wait=1)

    def check(self, page) -> bool:
        success = "Thank you for your request" in page
        page.click_close(wait=0.1)
        return success


class SavannahTaphouse(Script):

    URL = "https://savannahtaphouse.com/contact/"

    MESSAGES = [
        "You should treat your employees better.",
        "You should pay your employees more.",
        "You should protect your customers.",
    ]

    def run(self, page) -> pomace.Page:
        person = pomace.fake.person

        pomace.log.info("Filling form")
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_email(person.email)
        page.fill_message(random.choice(self.MESSAGES))

        pomace.log.info("Submitting form")
        page.browser.execute_script("window.scrollTo(0, 500);")

        return page.click_send_message()

    def check(self, page) -> bool:
        return "sent successfully" in page
