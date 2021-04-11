from abc import ABC, abstractmethod
from enum import Enum
from typing import List
from my_feed.modules.post import PostModel


# To ad a new social add a new entry on the enum
# they will be automatically handled
class PlatformsId(Enum):
    REDDIT = 'reddit'
    INSTAGRAM = 'instagram'
    TWITTER = 'twitter'


class PlatformInterface(ABC):

    def __init__(self):
        self._feed: List[PostModel] = []
        # ID of the last post get
        self._last_post_id = None

    def _set_feed(self, feed: List[PostModel]):
        self._feed = feed
        self._feed.reverse()

    @abstractmethod
    def __repr__(self) -> str:
        """
        :return: the str name of the platform from PlatformsId Enum
        """
        pass

    @staticmethod
    def _get_last_post_id(feed, last_update_id):
        """
        Update the last id of the new feed
        :param last_update_id: the id of the old update
        """
        if feed:
            # the feed is al list of post
            # Get the first (the newest) and make it the last post id
            return feed[0].id
        else:
            # if there are no new posts keep the current one
            return last_update_id

    @property
    def last_post_id(self):
        """
        The the last post Id
        This property must be get after the update
        :return: a slug ID
        """
        return self._last_post_id

    @abstractmethod
    def update(self, target, last_update_id) -> List[PostModel]:
        """
        Function that get the data from the platform api
        and set the last post_id
        :param target: the name of the channel
        :param last_update_id: the last post id known
        :return: a list of posts
        """
        pass
