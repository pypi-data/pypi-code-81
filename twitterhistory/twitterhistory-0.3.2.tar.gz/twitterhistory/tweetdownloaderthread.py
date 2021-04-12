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


"""Worker threads wrapping an APIDownloader."""


__all__ = ["TweetDownloaderThread"]


import datetime
import threading
import time

from .timespan import TimeSpan
from .tweetdownloader import (
    MonthlyQuotaExceededError,
    TemporaryApiResponseError,
    TweetDownloader,
)
from .database.apiresponsesaver import ApiResponseSaver


class TweetDownloaderThread(threading.Thread):
    """Wraps a TweetDownloader to run in a separate thread."""

    def __init__(self, api_key_manager, todo_deque, done_queue):
        """
        Intialize an PhotoDownloaderThread.

        Args:
            api_key_manager: instance of an ApiKeyManager
            todo_deque: collections.deque that serves (search_term, TimeSpan)
                        tuples that need to be downloaded
            done_queue: queue.Queue into which to put (search_term, TimeSpan)
                        tuples that have been downloaded

        """
        super().__init__()

        self._api_key_manager = api_key_manager
        self._todo_deque = todo_deque
        self._done_queue = done_queue

        self.shutdown = threading.Event()
        self.api_response_saver = ApiResponseSaver(self.shutdown)

    @property
    def count(self):
        """Count how many tweets we saved to the database"""
        try:
            count = self.api_response_saver.count
        except AttributeError:
            count = -1
        return count

    def run(self):
        """Get TimeSpans off todo_deque and download photos."""
        while not self.shutdown.is_set():
            try:
                search_term, timespan = self._todo_deque.pop()
                self._search_term = search_term
            except IndexError:
                break

            tweet_downloader = TweetDownloader(
                search_term, timespan, self._api_key_manager
            )

            earliest_tweet = timespan.end  # haven’t covered anything yet
            try:
                for batch in tweet_downloader.batches:
                    earliest_tweet = min(
                        earliest_tweet,
                        self.api_response_saver.save_batch(batch, search_term)
                    )

                    if self.shutdown.is_set():
                        timespan.start = earliest_tweet
                        break

            except TemporaryApiResponseError as exception:
                # (includes RateLimitExceededError)
                # report what we managed to download ...
                self._done_queue.put(
                    (search_term, TimeSpan(earliest_tweet, timespan.end))
                )

                # and remember what we haven’t been able to download
                timespan.end = earliest_tweet
                self._todo_deque.append((search_term, timespan))

                # then wait until we’re allowed again
                wait_seconds = (
                    exception.reset_time - datetime.datetime.now(datetime.timezone.utc)
                ).total_seconds()
                for _ in range(wait_seconds):
                    time.sleep(1)
                    if self.shutdown.is_set():
                        break
                else:
                    continue

            except MonthlyQuotaExceededError as exception:
                # TODO: report error properly,
                # for now, re-raise exception to escalte to parent thread
                raise exception from None

            # … report to parent thread how much we worked
            self._done_queue.put((search_term, timespan))
