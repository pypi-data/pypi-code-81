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


"""Download all tweets in a time span relating to a search query."""


__all__ = ["TweetDownloader"]


import datetime
import json

import requests


class ApiResponseError(BaseException):
    """Raised when API returns bogus data."""


class NoAcademicTwitterAccount(ApiResponseError):
    """Raised when API key not enrolled in academic API programme."""


class MonthlyQuotaExceededError(ApiResponseError):
    """Raised when API blocks because montly quota is used up."""


class TemporaryApiResponseError(ApiResponseError):
    """Raised when API has an error and waiting a bit should help"""

    def __init__(self, *args, time_until_reset=-1, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset_time = (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=time_until_reset)
        )

    def __str__(self):
        return "{:s}(reset_time={:%Y-%m-%d %H:%M:%S})".format(
            self.__class__.__name__, self.reset_time
        )

    def __repr__(self):
        return str(self)


class RateLimitExceededError(TemporaryApiResponseError):
    """Raised when API blocks because rate limit is reached."""


class TweetDownloader:  # pylint: disable=too-few-public-methods
    """Download all tweets in a time span relating to a search query."""

    API_ENDPOINT_URL = "https://api.twitter.com/2/tweets/search/all"

    def __init__(self, search_term, timespan, api_key_manager):
        """Intialize an TweetDownloader."""
        self._search_term = search_term
        self._timespan = timespan
        self._api_key_manager = api_key_manager

    @property
    def batches(self):
        """Iterate over downloaded batches of tweets + aux data."""
        query = {
            "query": self._search_term,
            "expansions": ",".join(
                [
                    #  "attachments.poll_ids",
                    "attachments.media_keys",
                    "author_id",
                    "entities.mentions.username",
                    "geo.place_id",
                    "in_reply_to_user_id",
                    "referenced_tweets.id",
                    "referenced_tweets.id.author_id",
                ]
            ),
            "media.fields": ",".join(
                [
                    #  "duration_ms",
                    #  "height",
                    #  "media_key",
                    #  "preview_image_url",
                    "type",
                    "url",
                    #  "width",
                    #  "public_metrics",
                    #  "non_public_metrics",
                    #  "organic_metrics",
                    #  "promoted_metrics"
                ]
            ),
            "place.fields": ",".join(
                [
                    #  "contained_within",
                    "country",
                    "country_code",
                    "full_name",
                    "geo",
                    "id",
                    "name",
                    "place_type",
                ]
            ),
            "tweet.fields": ",".join(
                [
                    "attachments",
                    "author_id",
                    # "context_annotations",
                    "conversation_id",
                    "created_at",
                    "entities",
                    "geo",
                    "id",
                    "in_reply_to_user_id",
                    "lang",
                    # "non_public_metrics",
                    # "public_metrics",
                    # "organic_metrics",
                    # "promoted_metrics",
                    "possibly_sensitive",
                    "referenced_tweets",
                    "reply_settings",
                    "source",
                    "text",
                    "withheld",
                ]
            ),
            "user.fields": ",".join(
                [
                    "created_at",
                    "description",
                    "entities",
                    "location",
                    "name",
                    "pinned_tweet_id",
                    "profile_image_url",
                    "protected",
                    # "public_metrics",
                    "url",
                    "username",
                    "verified",
                    "withheld",
                ]
            ),
            "start_time": self._timespan.start.isoformat(),
            "end_time": self._timespan.end.isoformat(),
            "max_results": 500,
        }
        next_token = None

        while True:
            if next_token is not None:
                query["next_token"] = next_token

            with self._api_key_manager.get_api_key() as api_key:
                headers = {"Authorization": "Bearer {:s}".format(api_key)}

                with requests.get(
                    self.API_ENDPOINT_URL, headers=headers, params=query
                ) as response:
                    try:
                        # some strings in Twitter API responses can apparently
                        # contain NUL characters that cause hickups in PostgreSQL
                        results = json.loads(
                            response.text
                            .replace("\\u0000", "\\u2400")
                        )
                    except json.decoder.JSONDecodeError as exception:
                        raise ApiResponseError(response.text) from exception

                    if not response.ok:
                        try:
                            if results["error"]["code"] == 88:
                                raise RateLimitExceededError(
                                    response.headers["x-rate-limit-reset"]
                                )
                        except KeyError:
                            pass

                        try:
                            if results["status"] == 429:
                                # results["title"]: "Too Many Requests"
                                # wait 2 min
                                raise TemporaryApiResponseError(
                                    time_until_reset=120
                                )
                        except KeyError:
                            pass

                        try:
                            if results["title"] == "UsageCapExceeded":
                                raise MonthlyQuotaExceededError()
                        except KeyError:
                            pass

                        try:
                            if results["reason"] == "client-not-enrolled":
                                raise NoAcademicTwitterAccount(results["detail"])
                        except KeyError:
                            pass

                        # other, not anticipated error:
                        raise ApiResponseError((results, response.headers))

            yield results

            try:
                next_token = results["meta"]["next_token"]
            except KeyError:
                break
