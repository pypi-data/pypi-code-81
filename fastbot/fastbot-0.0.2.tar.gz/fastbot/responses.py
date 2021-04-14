import enum
import json

from fastbot.json import JSONEncoder


class ContentType(enum.Enum):
    TEXT = "text"
    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"
    URL = "url"
    LOCATION = "location"
    FILE = "file"


class Data(object):

    def __init__(self, content_type=None,
                 url=None,
                 audio=None,
                 image=None,
                 video=None,
                 file=None,
                 latitude=None,
                 longitude=None,
                 text=None,
                 **kwargs):
        self.content_type = content_type
        self.url = url
        self.audio = audio
        self.image = image
        self.video = video
        self.latitude = latitude
        self.longitude = longitude
        self.text = text
        self.file = file

    def json(self):
        return json.dumps(self, cls=JSONEncoder)


class Request(Data):
    def __init__(self, channel_type=None, session=None, user=None, **kwargs):
        super(Request, self).__init__(**kwargs)
        self.channel_type = channel_type
        self.session = session
        self.user = user


class Response(Data):
    def __init__(self, session_type=None, **kwargs):
        super(Response, self).__init__(**kwargs)
        self.session_type = session_type


class EndResponse(Response):
    def __init__(self, **kwargs):
        super(EndResponse, self).__init__(session_type='END', **kwargs)


class ContinueResponse(Response):
    def __init__(self, **kwargs):
        super(ContinueResponse, self).__init__(session_type='CON', **kwargs)


class InitResponse(Response):
    def __init__(self, **kwargs):
        super(InitResponse, self).__init__(session_type='INIT', **kwargs)


def init(**kwargs):
    return InitResponse(**kwargs)


def end(**kwargs):
    return EndResponse(**kwargs)


def con(**kwargs):
    return ContinueResponse(**kwargs)
