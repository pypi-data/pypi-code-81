"""cloned from https://github.com/nalgeon/podsearch-py/blob/main/podsearch/"""
from typing import Optional
import json
import urllib.request
import urllib.parse
from urllib.error import (
    HTTPError,
    URLError,
)


def get(url: str, params: Optional[dict] = None) -> dict:
    """Perform HTTP GET request and return response as JSON"""
    try:
        query_str = urllib.parse.urlencode(params or {})
        req = urllib.request.Request(f"{url}?{query_str}")
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())
    except HTTPError as exc:
        raise Exception(f"HTTP error {exc.code}: {exc.reason}") from exc
    except URLError as exc:
        raise Exception(f"Network error: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise Exception(f"Failed to parse response: {exc}") from exc


from dataclasses import dataclass
from typing import List, Optional

BASE_URL = "https://itunes.apple.com"
SEARCH_URL = f"{BASE_URL}/search"
GET_URL = f"{BASE_URL}/lookup"
URL_TEMPLATE = "https://podcasts.apple.com/us/podcast/id{}"


@dataclass
class Podcast:
    """Podcast metadata."""
    id: str
    name: str
    author: str
    url: str
    feed: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None

class ItunesPodcast:
    """iTunes podcast description."""

    def __init__(self, source: dict):
        self._source = source

    def as_podcast(self) -> Podcast:
        """Converts iTunes description to Podcast object."""

        id_ = self._source["collectionId"]
        name = self._source["collectionName"]
        author = self._source["artistName"]
        url = URL_TEMPLATE.format(id_)
        podcast = Podcast(id=id_, name=name, author=author, url=url)
        podcast.feed = self._source.get("feedUrl")
        podcast.category = self._source.get("primaryGenreName")
        podcast.image = self._source.get("artworkUrl600")
        podcast.country = self._source.get("country")
        podcast.episode_count = self._source.get("trackCount")
        return podcast

class ItunesResults:
    """iTunes search results collection."""

    def __init__(self, source: dict):
        self.items = source.get("results", [])

    def as_podcasts(self) -> List[Podcast]:
        """Converts iTunes search results to Podcast list."""

        podcast_items = filter(ItunesResults._is_podcast, self.items)
        return [ItunesPodcast(item).as_podcast() for item in podcast_items]

    @staticmethod
    def _is_podcast(item):
        return item.get("wrapperType") == "track" and item.get("kind") == "podcast"


def search(name: str, limit: int = 5) -> List[Podcast]:
    """Search podcast by name"""
    params = {"term": name, "limit": limit, "media": "podcast"}
    response = get(url=SEARCH_URL, params=params)
    return ItunesResults(response)





