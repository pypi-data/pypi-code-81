#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2020 Christoph Fink, University of Helsinki
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 3
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.


"""Download (all) tweets."""


__all__ = ["BasicTwitterHistoryDownloader"]


import collections
import datetime
import queue
import math
import multiprocessing
import sys
import threading
import time

from .apikeymanager import ApiKeyManager
from .cache import Cache
from .cacheupdaterthread import CacheUpdaterThread
from .config import Config
from .tweetdownloaderthread import TweetDownloaderThread
from .sigtermreceivedexception import SigTermReceivedException
from .timespan import TimeSpan


class BasicTwitterHistoryDownloader:
    """Download (all) tweets."""

    NUM_WORKERS = multiprocessing.cpu_count()

    NUM_MANAGERS = 2  # main thread + cache_updater

    # if output into pipe (e.g. logger, systemd), then
    # print status every 10 minutes, else every 1/10 sec
    # also normal linefeed instead of carriage return for piped output
    STATUS_UPDATE_SEC = 0.1 if sys.stderr.isatty() else 600
    STATUS_UPDATE_LINE_END = "\r" if sys.stderr.isatty() else "\n"

    def __init__(self):
        """Intialise a BasicTwitterHistoryDownloader."""
        self.started = datetime.datetime.now()

        self._todo_deque = collections.deque()
        self._done_queue = queue.Queue()

        self._worker_threads = []
        self._cache_updater_thread = CacheUpdaterThread(self._done_queue)

        with Config() as config:
            self._api_key_manager = ApiKeyManager(
                [config["twitter_oauth2_bearer_token"]],
                300.0 / (15.0 * 60.0)  # 300/15 min,
                # https://developer.twitter.com/en/docs/twitter-api/tweets/
                # search/api-reference/get-tweets-search-all
            )

    def download(self):
        """Download all tweets."""
        with Config() as config:
            for search_term in config["search_terms"]:
                for gap in self.gaps_in_download_history(search_term):
                    self._todo_deque.appendleft((search_term, gap))

        try:
            # start downloaders
            for _ in range(self.NUM_WORKERS):
                worker = TweetDownloaderThread(
                    self._api_key_manager, self._todo_deque, self._done_queue
                )
                worker.start()
                self._worker_threads.append(worker)

            # start cache updater
            self._cache_updater_thread = CacheUpdaterThread(self._done_queue)
            self._cache_updater_thread.start()

            while threading.active_count() > self.NUM_MANAGERS:
                self.report_progress()
                time.sleep(self.STATUS_UPDATE_SEC)

        except (KeyboardInterrupt, SigTermReceivedException):
            self.announce_shutdown()
            for worker in self._worker_threads:
                worker.shutdown.set()

        finally:
            self.summarise_overall_progress()
            for worker in self._worker_threads:
                worker.join()
            self._cache_updater_thread.shutdown.set()
            self._cache_updater_thread.join()

    def report_progress(self):
        """Report current progress."""
        tweet_count, _ = self._statistics
        print(
            (
                "Downloaded metadata for {tweets: 6d} tweets "
                + "using {workers:d} workers, "
                + "{todo:d} time slots to cover"
            ).format(
                tweets=tweet_count,
                workers=(threading.active_count() - self.NUM_MANAGERS),
                todo=len(self._todo_deque),
            ),
            file=sys.stderr,
            end=self.STATUS_UPDATE_LINE_END,
            flush=True
        )

    @classmethod
    def announce_shutdown(cls):
        """Tell the user that we initiated shutdown."""
        print(
            "Cleaning up" + (" " * 69),  # 80 - len("Cleaning up")
            file=sys.stderr,
            end=cls.STATUS_UPDATE_LINE_END,
            flush=True
        )

    def summarise_overall_progress(self):
        """
        Summarise what we have done.

        (Called right before exit)
        """
        tweet_count, _ = self._statistics
        print(
            "Downloaded {tweets:d} tweets ".format(tweets=tweet_count),
            file=sys.stderr,
            flush=True
        )

    @staticmethod
    def gaps_in_download_history(search_term):
        """Find gaps in download history."""
        already_downloaded = BasicTwitterHistoryDownloader.already_downloaded_timespans(
            search_term
        )
        one_day = datetime.timedelta(days=1)  # for comparison

        for i in range(len(already_downloaded) - 1):
            gap = TimeSpan(already_downloaded[i].end, already_downloaded[i + 1].start)
            if gap.duration > one_day:
                divider = math.ceil(gap.duration / one_day)
                for part_of_gap in gap / divider:
                    yield part_of_gap
            else:
                yield gap

    @staticmethod
    def already_downloaded_timespans(search_term):
        """Figure out for which time spans we already have data."""
        with Cache() as cache:
            try:
                timespans = cache[search_term]["already downloaded"]
            except KeyError:
                timespans = []

        # delete existing 0-length time spans
        timespans = [
            timespan
            for timespan in timespans
            if timespan.duration > datetime.timedelta(0)
        ]

        # add 0-length time spans for
        # - first ever Tweet (https://twitter.com/jack/status/20)
        # - now()
        zero = datetime.datetime(2006, 3, 21, 22, 50, 0, tzinfo=datetime.timezone.utc)
        now = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
            minutes=1
        )
        timespans += [TimeSpan(zero, zero), TimeSpan(now, now)]

        return sum(timespans)  # sum resolves overlaps

    @property
    def _statistics(self):
        runtime = float((datetime.datetime.now() - self.started).total_seconds())

        tweet_count = sum(
            [
                worker.count
                for worker in self._worker_threads
                if isinstance(worker, TweetDownloaderThread)
            ]
        )
        tweet_rate = tweet_count / runtime

        return (tweet_count, tweet_rate)
