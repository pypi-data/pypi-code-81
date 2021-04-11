from typing import List
from types import DynamicClassAttribute
from enum import Enum
from datetime import datetime, timedelta

from my_feed.modules.post import PostModel

from my_feed.platforms import PlatformsId
from my_feed.platforms.reddit import Reddit
from my_feed.platforms.instagram import Instagram
# from my_feed.platforms.twitter import Twitter

# debug test of the lib
DEBUG = False


# To ad a new social add a new entry on the enum
# they will be automatically handled
class Platforms(Enum):
    REDDIT = (PlatformsId.REDDIT, Reddit)
    INSTAGRAM = (PlatformsId.INSTAGRAM, Instagram)
    # TWITTER = (PlatformsId.TWITTER, Twitter)

    @DynamicClassAttribute
    def identifier(self) -> PlatformsId:
        """The value of the Id in the enum member."""
        return self._value_[0]

    @DynamicClassAttribute
    def callable(self):
        """The value of the Class in the enum member."""
        return self._value_[1]

    @staticmethod
    def find_id(identifier: str):
        """
        Get the Platforms class by string Id
        :param identifier: the string name
        :return: a Platforms enum item
        :raise: KeyError if not found
        """
        for name, member in Platforms.__members__.items():
            if member.identifier.value == identifier:
                return member
        raise KeyError


class Source:

    def __init__(self, platform: Platforms, channel_id: str):

        # in case of a non existing channel set as disabled, so it will not update
        # if the fist call to the api is success set this true
        # if is false drop the channel
        self.exist = None

        # if the known channel is active or has been disabled by admins
        self.is_active = True

        # The platform update type (reddit, instagram, etc)
        self.platform: PlatformsId = platform.identifier
        self.updater = platform.callable  # the updater Class

        # initialize last update with an old time
        self.last_update: datetime = datetime.now() - timedelta(hours=5)
        # the exact time when the update start, to save it later
        self.__temp_last_update = None

        # update the data every minutes interval
        self.update_interval: int = 5

        # how to identify the last update, to not send again the same data
        # this value can be a string, slug, int or tuple based on the platform that you are using
        self.__last_update_id = None
        # temporally save the last update id
        self.__temp_last_update_id = None

        # the channel specification, this must match che update requirements in the platform api
        self.id: str = channel_id

    def __repr__(self):
        return f'{self.platform.value}/{self.id}'

    @property
    def is_time_to_update(self) -> bool:
        if datetime.now() - self.last_update > timedelta(minutes=self.update_interval) and self.is_active:
            return True
        return False

    def reset_last_update_id(self):
        self.__last_update_id = None

    def update(self) -> List[PostModel]:
        updater = self.updater()  # create the class
        out = updater.update(self.id, self.__last_update_id)
        self.__temp_last_update = datetime.now()

        # temporally save the last update id
        # after all the operations on the data are done call set_last_update_now()
        self.__temp_last_update_id = updater.last_post_id

        # if is the first time the last_update_id is none, so dont show any post
        if self.__last_update_id:
            return out
        else:
            return []

    def set_last_update_now(self) -> None:
        # update the last id, after all the operation on the data is done
        self.__last_update_id = self.__temp_last_update_id
        self.last_update = self.__temp_last_update

    def auto_update(self):
        """Auto update the feed, this can be done also manually"""
        out = []
        if self.is_time_to_update:
            out = self.update()
            self.set_last_update_now()
        return out
