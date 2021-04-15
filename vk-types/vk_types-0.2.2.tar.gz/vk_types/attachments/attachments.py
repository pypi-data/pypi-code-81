from enum import Enum
from typing import Optional, List
from ..base import BaseModel
from .photo import Photo, PostedPhoto
from .video import Video
from .audio import Audio
from .document import Document
from .graffiti import Graffiti
from .link import Link
from .note import Note
from .app import App
from .poll import Poll
from .page import Page
from .album import Album
from .market import Market
from .market_album import MarketAlbum
from .sticker import Sticker
from .pretty_cards import PrettyCards
from .event import Event


# https://vk.com/dev/objects/attachments_w


class Attachments(str, Enum):
    no_attachments = 0
    photo = Photo
    posted_photo = PostedPhoto
    video = Video
    audio = Audio
    document = Document
    graffiti = Graffiti
    link = Link
    note = Note
    app = App
    poll = Poll
    page = Page
    album = Album
    photos_list = List[int]
    market = Market
    market_album = MarketAlbum
    sticker = Sticker
    pretty_cards = PrettyCards
    event = Event


class Attachment(BaseModel):
    type: str
    photo: Optional[Photo]
    posted_photo: Optional[PostedPhoto]
    video: Optional[Video]
    audio: Optional[Audio]
    document: Optional[Document]
    graffiti: Optional[Graffiti]
    link: Optional[Link]
    note: Optional[Note]
    app: Optional[App]
    poll: Optional[Poll]
    page: Optional[Page]
    album: Optional[Album]
    photos_list: Optional[List[Photo]]
    market: Optional[Market]
    market_album: Optional[MarketAlbum]
    sticker: Optional[Sticker]
    pretty_cards: Optional[PrettyCards]
    event: Optional[Event]
