from typing import List
from .types import PostType


class MediaModel:

    def __init__(self, media_id, url):
        self.id = media_id
        self.url: str = url


class PostModel:

    def __init__(self, post_id, title, created_at, url):
        self.id: str = post_id
        self.title: str = title
        self.type: PostType = PostType.NONE
        self.created_at: str = created_at
        self.url: str = url
        self.media: List[MediaModel] = []
        self.description: str = ''

    def __repr__(self):
        return f'{self.url}'

    def add_media(self, media_id, media_url) -> None:
        """
        Append a new media to the Post
        """
        self.media.append(MediaModel(media_id, media_url))

    @property
    def is_text(self) -> bool:
        if self.type == PostType.TEXT:
            return True
        return False

    @property
    def is_embed(self) -> bool:
        if self.type == PostType.EMBED:
            return True
        return False

    @property
    def is_image(self) -> bool:
        if self.media and self.type == PostType.IMAGE:
            return True
        return False

    @property
    def is_video(self) -> bool:
        if self.media and self.type == PostType.VIDEO:
            return True
        return False

    @property
    def is_none(self) -> bool:
        if self.type == PostType.NONE:
            return True
        return False
