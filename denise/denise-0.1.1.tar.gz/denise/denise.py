import click
from enum import Enum
from time import sleep
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


ascii_ring = """
    __
  __\/__
 //----\\\\
||      ||
||      ||
 \\\\____//
   ----
"""


class Answers(Enum):
    YES = 1
    NO = 0


class Answer:
    def __init__(self, answer: str):
        self.answer = answer.lower()

    def parse(self):
        if self.answer == "y":
            return Answers.YES
        return Answers.NO


def get_years_since_anniversary():
    return (datetime.now() - datetime(2014, 8, 30)).days // 365


def print_and_sleep(to_print: str):
    average_reading_speed = 75
    expected_rate = average_reading_speed / 60
    print(to_print)
    time_to_sleep = len(to_print.split()) * 0.7
    #print("sleeping for %s seconds", time_to_sleep)
    sleep(time_to_sleep)


def start_fun():
    print_and_sleep("Hey butts")
    print_and_sleep("Its Matt")
    print_and_sleep(f"We've been dating for {get_years_since_anniversary()} years")
    print_and_sleep("Even though we've been so far away for most of the time and the pandemic has put a damper "
                    "on things.")
    print_and_sleep("You've always been there to support me and give me encouragement through school and work.")
    print_and_sleep("I don't know what I would have done without you.")
    print_and_sleep("I wish I could be there with you in person to give you the real thing, "
                    "but at the moment this is the best I can do.")
    sleep(2)
    print(ascii_ring)
    return Answer(input("Will you marry me?"))


def stop_fun():
    pass


def is_denise(answer: Answer):
    if answer.parse():
        return start_fun()
    return stop_fun()


@click.command()
def love():
    answer = Answer(input("Is your name Denise? [y]/n ") or "Y")
    is_denise(answer)


def start():
    love()
