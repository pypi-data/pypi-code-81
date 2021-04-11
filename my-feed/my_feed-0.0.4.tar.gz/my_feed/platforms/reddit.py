import json
import requests
from enum import Enum

from my_feed.platforms import PlatformInterface, PlatformsId
from my_feed.modules.post import PostModel
from my_feed.modules.types import PostType

# header for the requests to the reddit api
HEADER = {'User-agent': 'bot'}


class Reddit(PlatformInterface):

    class __RedditPostTypes(Enum):
        SELF = 'self'
        REDDIT_VIDEO = 'reddit:video'
        HOSTED_VIDEO = 'hosted:video'
        VIDEO = 'rich:video'
        IMAGE = 'image'
        LINK = 'link'
        NONE = None

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return PlatformsId.REDDIT.value

    @staticmethod
    def __request_data(r):
        """
        Call the reddit api for the data
        :param r: the sub-reddit
        :return: the data as dictionary
        :raise ConnectionError: if the api don't respond with a 200
        """

        url = f'https://www.reddit.com/r/{r}/top.json?limit=15'

        res = requests.get(url, headers=HEADER)
        if res.status_code == 200:
            json_data = res.content
            return json.loads(json_data).get('data')
        else:
            raise ConnectionError

    def __build_feed(self, feed_data, last_update_id):
        """
        :param feed_data: the data coming from the reddit api
        :param last_update_id: the last post id received (eg: t1-sxsdfew")
        :return: list of feed
        """

        out = []
        posts = feed_data.get('children')

        for el in posts:

            data = el.get('data')

            # check if the last post is the recent one
            post_id = data.get('name')
            if post_id == last_update_id:
                break

            # create the std post object
            # with the base data
            post = PostModel(
                post_id=post_id,
                title=data.get('title'),
                created_at=data.get('created_utc'),
                url='https://www.reddit.com%s' % data.get('permalink')
            )

            # reddit way to define what type of post is it
            post_hint = data.get('post_hint')
            try:
                post_type_hint = self.__RedditPostTypes(post_hint)
            except Exception as exc:
                print(exc)
                post_type_hint = self.__RedditPostTypes.NONE

            # the post has video extract the video
            # the video on reddit can be only one per post
            if data.get('media'):
                post.type = PostType.EMBED
                post.add_media(
                    media_id=data.get('id'),
                    media_url=data.get('url')
                )

            # if the post don't have a video in it, check for images
            # the images on reddit can be more than one per post (loop?)
            elif data.get('preview'):
                # the post contains just a link, and reddit is not able to load it as embed
                if post_type_hint == self.__RedditPostTypes.LINK:
                    post.type = PostType.EMBED
                else:
                    post.type = PostType.IMAGE
                post.add_media(
                    media_id=data.get('id'),
                    media_url=data.get('url')
                )

            # if the post don't contains neither video or image it should tbe a text post
            else:
                post.type = PostType.TEXT

            # check if there are a description in the post
            # the caption text aside the title
            description = data.get('selftext')
            if description:
                post.description = description

            out.append(post)  # add the post to the out

        return out

    def update(self, r, last_update_id):
        """
        :param r: the sub-reddit channel
        :param last_update_id: the id of the last known post
        :return: a list of feed data
        """
        data = self.__request_data(r)
        feed = self.__build_feed(data, last_update_id)

        # get the post id from the feed
        last_post_id = self._get_last_post_id(feed, last_update_id)

        # the set feed will also revert it
        self._set_feed(feed)
        # update the post id
        self._last_post_id = last_post_id

        return self._feed
