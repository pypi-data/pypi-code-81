from __future__ import print_function
import pickle
import argparse
import logging
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import sys
import pytz

SEARCH_INTERVAL = 12
now = datetime.datetime.now

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    handlers=[
        logging.StreamHandler(),
    ])
logger = logging.getLogger()


def deduplicate_events(events, existing_events):
    to_delete = []
    tz = pytz.timezone('Europe/Kiev')
    for event in events:
        for existing_event in existing_events:
            ename = existing_event['summary']
            cname = event['summary']
            if ename == cname:
                if 'dateTime' in event['start']:
                    cstart = tz.localize(datetime.datetime.strptime(event['start']['dateTime'], "%Y-%m-%dT%H:%M:%S"))
                    cend = tz.localize(datetime.datetime.strptime(event['end']['dateTime'], "%Y-%m-%dT%H:%M:%S"))
                    estart = datetime.datetime.strptime(existing_event['start']['dateTime'], "%Y-%m-%dT%H:%M:%S%z")
                    eend = datetime.datetime.strptime(existing_event['end']['dateTime'], "%Y-%m-%dT%H:%M:%S%z")
                elif 'date' in event['start']:
                    cstart = datetime.datetime.strptime(event['start']['date'], "%Y-%m-%d")
                    cend = datetime.datetime.strptime(event['end']['date'], "%Y-%m-%d")
                    estart = datetime.datetime.strptime(existing_event['start']['date'], "%Y-%m-%d")
                    eend = datetime.datetime.strptime(existing_event['end']['date'], "%Y-%m-%d")
                if estart == cstart and eend == cend:
                    print("{} - {} - Event exists!".format(cname, cstart))
                    # print('ename:{}\ncname:{}\nestart:{}\ncstart:{}\neend:{}\ncend:{}\n'.format(ename, cname, estart, cstart, eend, cend))
                    to_delete.append(event)
    return [x for x in events if x not in to_delete]


def create_events(service, calendar, events, deduplication=True, search_interval=24*7):
    if deduplication:
        existing_events = get_events(service, calendar, search_interval)
        events = deduplicate_events(events, existing_events)
    for event in events:
        if 'date' in event['start']:
            sdate = event['start']['date']
            edate = event['end']['date']
        else:
            sdate = event['start']['dateTime']
            edate = event['end']['dateTime']
        print("Event:{} -- description:{} -- start:{} end:{}".format(
            event['summary'],
            event['description'],
            sdate,
            edate
        ))
        service.events().insert(calendarId=calendar, body=event).execute()


def create_single_event(service, calendar, name, description, start=now, end=now, deduplication=True):
    event = {
      'summary': name,
      'description': description,
      'start': {
        'dateTime': start,
        'timeZone': 'Europe/Kiev',
      },
      'end': {
        'dateTime': end,
        'timeZone': 'Europe/Kiev',
      }
    }
    service.events().insert(calendarId=calendar, body=event).execute()
    logger.info('{}: created!'.format(name))


def create_single_day_event(service, calendar, name, description, start=now, end=now, deduplication=True):
    # "yyyy-mm-dd"
    event = {
      'summary': name,
      'description': description,
      'start': {
        'date': start,
        'timeZone': 'Europe/Kiev',
      },
      'end': {
        'date': end,
        'timeZone': 'Europe/Kiev',
      }
    }
    service.events().insert(calendarId=calendar, body=event).execute()
    logger.info('{}: created!'.format(name))


def get_events(service, calendar, search_interval=SEARCH_INTERVAL):
    # TODO: strange time drifts
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId=UES, timeMin=now_plus, timeMax=now_minus,
    now_minus_raw = datetime.datetime.utcnow() - datetime.timedelta(hours=search_interval)
    now_minus = now_minus_raw.isoformat() + 'Z'
    events_result = service.events().list(
        calendarId=calendar, timeZone='Europe/Kiev', timeMin=now_minus,
        maxResults=50, singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        logger.info('No events found')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # logger.info('%s %s', start, event['summary'])
    return events


def extend_event(service, calendar, search_event, name, description, search_interval=SEARCH_INTERVAL, change_start=False):
    events = get_events(service, calendar, search_interval)
    found_events = []
    for event in events:
        if event['summary'] == search_event:
            logger.info('found {} event: {}'.format(search_event, event['id']))
            found_events.append(event['id'])
    if not found_events:
        logger.info('cant find {} event in last {} hours'.format(search_event, search_interval))
        return False
    else:
        last_event = found_events[-1:]
        logger.info('Using the last one {} event'.format(last_event[0]))
        modify_event = service.events().get(calendarId=calendar, eventId=last_event[0]).execute()
        if change_start:
            modify_event['start']['dateTime'] = now
        modify_event['summary'] = name
        modify_event['description'] = description
        modify_event['end']['dateTime'] = now
        logger.info('updating event id: {}'.format(modify_event['id']))
        service.events().update(calendarId=calendar, eventId=last_event[0], body=modify_event).execute()
        logger.info('updated!')
        return True

