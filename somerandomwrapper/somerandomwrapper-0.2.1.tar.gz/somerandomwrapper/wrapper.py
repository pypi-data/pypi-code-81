from typing import Optional

from googletrans import Translator
from requests import get


class SomeRandomWrapper:
    def __init__(self):
        self.base_url = 'https://some-random-api.ml'
        self.translator = Translator()

    async def get_fact(self, animal_object: str = 'dog', translate: bool = False, dest: Optional[str] = None):
        request = get(f'{self.base_url}/facts/{animal_object}').json()

        if translate:
            api_fact = str(request['fact'])
            return {'fact_translated': self.translator.translate(api_fact, src='en', dest=dest)}

        return str(request['fact'])

    async def get_image(self, animal_type: str = 'dog'):
        request = get(f'{self.base_url}/img/{animal_type}').json()
        return str(request['link'])

    async def get_animu(self, image_type: str = 'wink'):
        request = get(f'{self.base_url}/animu/{image_type}').json()
        return request['link']

    async def get_canvas(self, canvas: str = None, avatar: str = None):
        return f'{self.base_url}/canvas/{canvas}?avatar={avatar}'

    async def get_youtube_comment(self, username: str = None, avatar: str = None, comment: str = None):
        return f'{self.base_url}/canvas/youtube-comment?avatar={avatar}&username={username}&comment={comment}'

    async def get_color(self, hex_color: str = '#FFFFFF'):
        return f'{self.base_url}/canvas/colorviewer?hex={hex_color}'

    async def get_hex(self, rgb_color: str = '255,255,255'):
        request = get(f'{self.base_url}/canvas/hex?rgb={rgb_color}').json()
        return request['hex']

    async def get_lyrics(self, song_title: str = 'Never Gonna Give You Up'):
        request = get(f'{self.base_url}/lyrics?title={song_title}').json()
        return {'song_title': request['title'], 'song_author': request['author'],
                'song_cover_image': request['thumbnail']['genius'],
                'song_lyrics': request['lyrics']}
