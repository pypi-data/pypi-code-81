#!/usr/bin/python
import psycopg2
import sys

from configparser import ConfigParser
from mail import prepare_mail


def config(filename="runner/database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return db


def get_mails():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute("SELECT email from mail;")
        mails = cur.fetchall()
        res = []
        for mail in mails:
            res.append(mail[0])

        # close the communication with the PostgreSQL
        cur.close()
        return res
    except (Exception, psycopg2.DatabaseError) as error:
        print(error, file=sys.stderr)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


def send_all(size, lg="en"):
    for mail in get_mails():
        prepare_mail(mail, size, lg)
