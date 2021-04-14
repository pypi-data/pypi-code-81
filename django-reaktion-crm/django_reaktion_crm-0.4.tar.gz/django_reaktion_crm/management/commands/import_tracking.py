import pytz
import os
import csv
import psycopg2
from icecream import ic
from pymongo import MongoClient  # type: ignore
from datetime import datetime, timedelta
from urllib.parse import urlparse
from sentry_sdk import capture_message

from django.core.management.base import BaseCommand

from django_reaktion_crm.models import Visits
from django_reaktion_crm.models import Clients

debug = False

conn = os.environ['MONGO_CONN']
client = MongoClient(conn)

my_db_tracking = client['tracking-prod']
tz = pytz.timezone('Europe/Stockholm')


def agg_last_visits(uid, days, domain_id):
    now = datetime.now(tz=tz)
    start = now - timedelta(days)

    count = my_db_tracking['trackings'].aggregate([
        {
            '$match': {
                'uid': uid,
                'domain_id': domain_id,
                'createdAt': {
                    '$gte': start
                }
            }
        }, {
            '$count': 'domain_id'
        }
    ])
    for i in count:
        return i['domain_id']

    return 0


def agg_last_7_days_visits(uid, domain_id):
    return agg_last_visits(uid, 7, domain_id=domain_id)


def agg_last_30_days_visits(uid, domain_id):
    return agg_last_visits(uid, 30, domain_id=domain_id)


def agg_all_visits(uid, domain_id):
    return Visits.objects.filter(uid=uid).count()


def last_user_visit(uid):
    """
    TODO
    :param uid:
    :return:
    """
    pass


def agg_user_visits_by_day(uid, day):
    """
    TODO
    :param uid:
    :param day:
    :return:
    """
    pass


def create_error_reports(domain_id, unregistered, unregistered_unique):
    print("raport nr 1")
    with open('unregister_full.csv', mode='w') as csv_file:
        fieldnames = ['url', 'uid', 'created']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for item in unregistered:
            writer.writerow({'url': item['url'], 'uid': item['uid'], 'created': item['createdAt']})

    """
    unregister - unique uid
    """
    print("raport nr 2")
    print(unregistered_unique)
    with open('unregister_only_uid.csv', mode='w') as csv_file:
        fieldnames = ['uid']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for item in unregistered_unique:
            writer.writerow({'uid': item})

    """
    postgres
    """
    still_active = []

    result = urlparse(os.environ['REAKTION_DB'])
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    conn = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )

    cur = conn.cursor()

    for item in unregistered_unique:
        q = f"SELECT is_active from subscriptions where email_id = {item} and domain_id = {domain_id}"
        cur.execute(q)
        data = cur.fetchall()
        for d in data:
            print(d[0])
            if d[0] is True:
                print(item)
                q2 = f"SELECT email from emails where id = {item}"
                cur.execute(q2)
                data_email = cur.fetchall()
                for e in data_email:
                    still_active.append(e[0])

    conn.close()

    final_csv_name = f"unregister_emails_{domain_id}.csv"

    with open(final_csv_name, mode='w') as csv_file:
        fieldnames = ['email']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for item in still_active:
            writer.writerow({'email': item})

    print("Reports created")


class Command(BaseCommand):
    help = 'Import latest activity from tracking database'

    def add_arguments(self, parser):
        parser.add_argument('delta', nargs='+', type=str)

    def handle(self, *args, **options):

        collection_impressions_agg = my_db_tracking['trackings']

        missing_clients = []
        wrong_base_64 = []
        unregistered = []
        unregistered_unique = []

        """
        Set up date
        """
        now = datetime.utcnow()
        if options['delta']:
            hours = int(options['delta'][1])
        else:
            hours = 4

        start_date = now - timedelta(hours=hours)
        domain_id = int(os.environ['DOMAIN_ID'])

        now = pytz.utc.localize(now)
        start_date = pytz.utc.localize(start_date)
        """
        delete for period
        """
        Visits.objects.filter(created_at__range=[start_date, now]).delete()

        """
        Take all trakcings
        """
        ic(start_date)
        ic(now)
        ic(domain_id)

        cursor_agg_impressions = collection_impressions_agg.find({'domain_id': domain_id, 'createdAt': {
            '$gte': start_date,
            '$lt': now
        }})

        for post in cursor_agg_impressions:

            if post['uid'] is None:
                continue

            uid = post['uid']

            """
            Add to visits table
            """
            aware_date = pytz.utc.localize(post['createdAt'])
            """
            todo: not save if uid is empty
            """
            if Clients.objects.filter(uid=uid).count():
                if len(post['url']) > 255:
                    post['url'] = post['url'][:255]

                ic(post['url'])

                visits = Visits(uid=uid, url=post['url'], created_at=aware_date)
                visits.save()
            else:
                continue

            if "avprenumerera/?ok" in post['url']:
                unregistered.append(post)
                unregistered_unique.append(post['uid'])
                try:
                    person = Clients.objects.filter(uid=uid).get()
                    person.active = False
                    person.save()
                except Clients.DoesNotExist:
                    print("Missing uid")

            try:
                """
                find -7 and -30 days visits                
                """
                last_7_days = agg_last_7_days_visits(uid, domain_id=domain_id)
                last_30_days = agg_last_30_days_visits(uid, domain_id=domain_id)
                all_visits = agg_all_visits(uid, domain_id=domain_id)

                """
                Update user data
                """
                find_client_by_uid = Clients.objects.filter(uid=uid).get()
                find_client_by_uid.all_visits = all_visits
                find_client_by_uid.last_visit = aware_date
                find_client_by_uid.last_7_days_visits = last_7_days
                find_client_by_uid.last_30_days_visits = last_30_days
                find_client_by_uid.save()

            except Clients.DoesNotExist:
                missing_clients.append(uid)
                continue
            except Clients.MultipleObjectsReturned:
                print(f"Duplicated clients {post['uid']}")
                wrong_base_64.append(uid)
                exit(0)
            except Clients.DataError:
                pass

        if debug is True:
            create_error_reports(domain_id, unregistered, unregistered_unique)

        if os.environ['DJANGO_ENV'] == "dev":
            capture_message('Import finished')
