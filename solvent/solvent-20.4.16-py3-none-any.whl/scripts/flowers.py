import random

import pomace

from . import Script


class Flowers(Script):

    URL = "https://www.beckysflowersmidland.com/contacts.html"

    def run(self, page) -> pomace.Page:
        person = pomace.fake.person
        page.fill_date(pomace.fake.future_date.strftime("%m/%d/%Y"))
        page.fill_full_name(person.first_name + " " + person.last_name)
        page.fill_email(person.email)
        page.fill_message(
            random.choice(
                [
                    "https://twitter.com/Cleavon_MD/status/1347334743323394048",
                    "https://www.instagram.com/p/CJw0GrLHazm/",
                ]
            )
        )
        return page.click_submit_request()

    def check(self, page) -> bool:
        return page.url != self.URL
