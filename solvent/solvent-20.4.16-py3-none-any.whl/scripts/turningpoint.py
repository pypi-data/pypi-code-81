import random

import log
import pomace

from . import Script

MESSAGES = [
    "I'd like to learn how I can help out.",
    "This is important to me. Where can I donate?",
    "What's the best way to send you money?",
    "Who can I talk to about donating?",
    "My company is interested in sponsoring you. Can you give me a call?",
]


class TurningPoint(Script):

    URL = "https://www.tpusa.com"
    URL = "https://fs21.formsite.com/res/showFormEmbed?EParam=m_OmK8apOTC0KL4MVNYdx3SKlBogGjHGFzpUCZwnDno&317718171&EmbedId=317718171"

    def run(self, page) -> pomace.Page:
        person = pomace.fake.person

        log.info(f"Beginning iteration as {person}")

        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_email_address(person.email_address)
        page.fill_phone_number(person.phone_number)

        page.click_state(wait=0)
        try:
            page.browser.find_by_text(person.state).click()
        except:
            return page

        page.fill_zip_code(person.zip_code)

        page.click_phone(wait=0)
        page.click_sponsorships(wait=0)
        page.fill_message(random.choice(MESSAGES))
        page = page.click_submit()

        return page

    def check(self, page) -> bool:
        return "success" in page.url
