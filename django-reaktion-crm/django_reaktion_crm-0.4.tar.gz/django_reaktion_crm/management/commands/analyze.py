import pytz
import os
import csv
import re
import psycopg2
from pymongo import MongoClient  # type: ignore
from datetime import datetime, timedelta
from urllib.parse import urlparse
from sentry_sdk import capture_message

from django.core.management.base import BaseCommand

from django_reaktion_crm.models import Visits
from django_reaktion_crm.models import Clients
from django_reaktion_crm.models import Newsletter, NewsletterLink
from icecream import ic

"""
Take last newsletter links 
"""

"""
users_links = [
    {
        registered_url: "",
        clicked_the_same_date: F/T,
        has_uid: F/T    
    }
]
"""


class Command(BaseCommand):
    help = 'Analyze if bots clicked in email'

    def __init__(self):
        self.current_links = []
        self.newsletter_date = ""
        self.hits_level = 85
        self.bots = []
        self.remove_from_bots = []
        self.all_analyzed_uids = 0

    def analyze_url(self, user_url):
        """
        has uid,
        was clicked the same day as newsletter was send
        """

        analyzed_url = {}
        analyzed_url['has_uid'] = False
        analyzed_url['has_newsletter_date'] = False
        analyzed_url['is_newsletter_url'] = False
        analyzed_url['url'] = user_url[0]

        for item in self.current_links:

            if re.search(item, user_url[0]):
                analyzed_url['is_newsletter_url'] = True

                if re.search('/?uid=', user_url[0]):
                    analyzed_url['has_uid'] = True

                # Date

                if user_url[1] == self.newsletter_date:
                    analyzed_url['has_newsletter_date'] = True

        return analyzed_url

    def get_users_links(self, uid):
        user_payload = Visits.objects.filter(uid=uid).filter(created_at__gte=self.newsletter_date)
        user_links = [[link.url, link.created_at.date(), link.created_at.strftime('%y-%m-%d')] for link in user_payload]
        return user_links

    def get_users_uids(self):
        # Select * visits after the latest newsletter was send
        uids = Visits.objects.filter(created_at__gte=self.newsletter_date).distinct('uid')
        selected_uids = [item.uid for item in uids]
        self.all_analyzed_uids = len(selected_uids)
        return selected_uids

    def get_user_by_uid(self, uid):
        user = Clients.objects.filter(uid=uid).get()
        return user.email

    def analyze_stats(self, urls):
        count_all = 0
        count_has_uid = 0
        count_is_newsletter_url = 0
        count_has_newsletter_date = 0

        for item in urls:
            if item['has_newsletter_date'] == True:
                count_has_newsletter_date = count_has_newsletter_date + 1
            if item['has_uid'] == True:
                count_has_uid = count_has_uid + 1
            if item['is_newsletter_url'] == True:
                count_is_newsletter_url = count_is_newsletter_url + 1

            count_all = count_all + 1

        return {
            'all': count_all,
            'uid': count_has_uid,
            'uid_proc': (count_has_uid / count_all) * 100,
            'date': count_has_newsletter_date,
            'date_proc': (count_has_newsletter_date / count_all) * 100,
            'url': count_is_newsletter_url,
            'url_proc': (count_is_newsletter_url / count_all) * 100
        }

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """ Latest newsletter """
        newsletter = Newsletter.objects.latest('created')
        newsletter_date = newsletter.created_at

        self.newsletter_date = newsletter_date.date()

        newsletter_links = NewsletterLink.objects.filter(newsletter__id=newsletter.id)
        self.current_links = [link.link for link in newsletter_links]

        latest_users = self.get_users_uids()

        for uid in latest_users:
            user_links = self.get_users_links(uid)

            group_links_by_day = {}

            for item in user_links:

                my_key = item[2].replace("-", "")

                if my_key in group_links_by_day:
                    group_links_by_day[my_key] = group_links_by_day[my_key] + 1
                else:
                    group_links_by_day[my_key] = 1

            points = 0

            analyzed_urls = []

            for item in user_links:
                analyzed_urls.append(self.analyze_url(item))

            stats = self.analyze_stats(analyzed_urls)

            if stats['all'] >= len(self.current_links):
                if stats['date_proc'] > self.hits_level and \
                        stats['uid_proc'] > self.hits_level and \
                        stats['url_proc'] > self.hits_level:
                    self.bots.append(uid)
                else:
                    self.remove_from_bots.append(uid)

            else:

                if stats['url_proc'] > 90:
                    self.bots.append(uid)
                    pass
                else:
                    self.remove_from_bots.append(uid)

            """
            Analyze stats for every uid
            """

        remove_dup = len(set(self.bots))

        if os.environ['DJANGO_ENV'] == "dev":
            ic(set(self.bots))
            ic(self.all_analyzed_uids)

        c = (remove_dup / self.all_analyzed_uids) * 100
        emails = [self.get_user_by_uid(item) for item in self.bots]

        if os.environ['DJANGO_ENV'] == "dev":
            ic(c)
            ic(emails)
            ic(self.remove_from_bots)

        """
        deactivate bot-like-emails
        """
        for bot in self.bots:
            c = Clients.objects.filter(uid=bot).first()
            c.bot = 1
            c.save()

        for bot in self.remove_from_bots:
            c = Clients.objects.filter(uid=bot).first()
            c.bot = 0
            c.save()

        if os.environ['DJANGO_ENV'] == "dev":
            ic("done")
