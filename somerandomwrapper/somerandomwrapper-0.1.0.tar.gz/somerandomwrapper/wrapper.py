from json import loads
from typing import Optional
from http3 import AsyncClient
from googletrans import Translator


class SomeRandomWrapper:
	def __init__(self):
		self.base_url = 'https://some-random-api.ml'
		self.translator = Translator()
		self.http_client = AsyncClient()


	async def get_fact(self, animal_object: str = 'dog', translate: bool = False, dest: Optional[str] = None):
		try:
			request = await self.http_client.get(f'{self.base_url}/facts/{animal_object}')
			request_json = loads(str(request.text))
		except RuntimeError:
			return {'is_error': True, 'error_description': 'External SomeRandomAPI error.'}

		if 'error' in request_json or request.status_code != 200:
			return {'is_error': True, 'error_description': request_json['error']}
		elif translate:
			api_fact = str(request_json['fact'])
			return {'fact_original': api_fact, 'fact_translated': self.translator.translate(api_fact, src='en', dest=dest)}
		
		return str(request_json['fact'])


	async def get_image(self, animal_object: str = 'dog'):
		try:
			request = await self.http_client.get(f'{self.base_url}/img/{animal_object}')
			request_json = loads(str(request.text))
		except RuntimeError:
			return {'is_error': True, 'error_description': 'External SomeRandomAPI error.'}

		if 'error' in request_json or request.status_code != 200:
			return {'is_error': True, 'error_description': request_json['error']}
		
		return str(request_json['link'])


	async def get_animu(self, atype: str = 'wink'):
		try:
			request = await self.http_client.get(f'{self.base_url}/animu/{atype}')
			request_json = loads(str(request.text))
		except RuntimeError:
			return {'is_error': True, 'error_description': 'External SomeRandomAPI error.'}

		return request_json['link']


	async def get_canvas(self, canva, avatar):
		return f'{self.base_url}/canvas/{canva}?avatar={avatar}'


	async def get_youtube_comment(self, username: str = 'julheer', avatar: str = '', comment: str = 'Hello, world!'):
		return f'{self.base_url}/canvas/youtube-comment?avatar={avatar}&username={username}&comment={comment}'


	async def get_color(self, ahex: str = '#FFFFFF'):
		return f'{self.base_url}/canvas/colorviewer?hex={ahex}'


	async def get_hex(self, argb: str = '255,255,255'):
		try:
			request = await self.http_client.get(f'{self.base_url}/canvas/hex?rgb={argb}')
			request_json = loads(str(request.text))
		except RuntimeError:
			return {'is_error': True, 'error_description': 'External SomeRandomAPI error.'}

		return request_json['hex']


	async def get_lyrics(self, song_title: str = 'Never Gonna Give You Up'):
		try:
			request = await self.http_client.get(f'{self.base_url}/lyrics?title={song_title}')
			request_json = loads(str(request.text))
		except RuntimeError:
			return {'is_error': True, 'error_description': 'External SomeRandomAPI error.'}

		return request_json['lyrics']
