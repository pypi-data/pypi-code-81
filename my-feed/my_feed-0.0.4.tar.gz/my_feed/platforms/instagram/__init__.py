from enum import Enum
from my_feed.modules.post import PostModel
from my_feed.modules.types import PostType
from my_feed.platforms import PlatformInterface, PlatformsId
from my_feed.platforms.instagram.credentials import credentials_manager
from my_feed.platforms.instagram.login import InstagramLogin


class MediaType(Enum):
    video = 'video'
    image = 'image'


class Instagram(PlatformInterface):

    def __init__(self):
        super().__init__()

        self.api: InstagramLogin

    def __repr__(self):
        return PlatformsId.INSTAGRAM.value

    def _login(self):
        user = credentials_manager.credentials[0]
        il = InstagramLogin()
        self.api = il.login(user.username, user.password, 'configs/{}_creds.json'.format(user.username))

    @staticmethod
    def get_media_url(media_data):
        media = media_data.get('standard_resolution', {})
        return media.get('url')

    def story(self, user_id, last_update_id) -> [PostModel]:
        """
        story can be get only if you are logged in
        Load all the stories from the user loaded
        :return: InstagramStory list
        """
        out = []  # list of all the items in the story

        stories = self.api.user_story_feed(user_id)

        reels = stories.get('reel')
        if not reels:
            return []

        reels = reels.get('items')
        for reel in reels:

            post_id = reel.get('pk')
            if post_id == last_update_id:
                break

            post = PostModel(
                post_id=post_id,
                title='',
                created_at=reel.get('taken_at'),
                url=reel.get('link')
            )

            media_type = MediaType(reel.get('type'))
            post.type = PostType.VIDEO if media_type == MediaType.video else PostType.IMAGE
            media = reel.get('videos' if media_type == MediaType.video else 'images')
            post.add_media(media_id=None, media_url=self.get_media_url(media))

            out.append(post)

        return out

    def post(self, user_id, last_update_id) -> [PostModel]:
        """
        Get all the post from the user loaded
        Store them as a list of InstagramPost obj
        :return: PostModel list
        """
        out = []

        media = self.api.user_feed(user_id)

        items = media.get('items')
        for item in items:

            post_id = item.get('code')
            if post_id == last_update_id:
                break

            # get description of the post
            caption = item.get('caption', {})
            text = ''
            if caption:
                text = caption.get('text', '')

            post = PostModel(
                post_id=post_id,
                title=text,
                created_at=item.get('created_time'),
                url=item.get('link')
            )

            """
            Check if is a post with multiple elements
                - multi element post has media list inside carousel_media
                - if not the object media is no encapsulated
            """
            carousel = item.get('carousel_media')
            media_type = MediaType(item.get('type'))
            post.type = PostType.VIDEO if media_type == MediaType.video else PostType.IMAGE
            if carousel:
                for c in carousel:
                    media = c.get('videos' if media_type == MediaType.video else 'images')
                    post.add_media(media_id=None, media_url=self.get_media_url(media))

            else:
                media = item.get('videos' if media_type == MediaType.video else 'images')
                post.add_media(media_id=None, media_url=self.get_media_url(media))

            out.append(post)

        return out

    def update(self, target, last_update_id):

        # decouple the last update id
        # this cause instagram have 2 feed sources, stories and posts
        last_update_id_story = None
        last_update_id_post = None
        if last_update_id:
            last_update_id_story, last_update_id_post = last_update_id

        # do login every time
        self._login()

        # get the data from the api
        story_feed = self.story(target, last_update_id_story)
        post_feed = self.post(target, last_update_id_post)

        # get the post id from the feed
        last_update_id_story = self._get_last_post_id(story_feed, last_update_id_story)
        last_update_id_post = self._get_last_post_id(post_feed, last_update_id_post)

        # the set feed will also revert it
        self._set_feed(post_feed + story_feed)

        # update the post id
        self._last_post_id = (last_update_id_story, last_update_id_post)
        return self._feed
