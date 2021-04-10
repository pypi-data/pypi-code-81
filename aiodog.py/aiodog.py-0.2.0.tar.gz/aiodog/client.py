__all__ = ('Client',)

import aiohttp
from functools import partialmethod
from json import JSONDecodeError
from typing import Any, Dict, List, Optional, Union


from dog.client import _get_url
from dog.models import Breed, Category, Favourite, Image, ImageAnalysis, PartialImage, Vote

RequestResponse = Union[Dict[str, Any], str]

async def try_json(response: aiohttp.ClientResponse):
    response.raise_for_status()
    try:
        return await response.json()
    except JSONDecodeError:
        return await response.text()

class Client:
    def __init__(self, api_key: Optional[str] = None, *, session: Optional[aiohttp.ClientSession] = None) -> None:
        self.api_key = api_key
        self._session = None

    async def request(self, method: str, route: str, **kwargs) -> RequestResponse:
        headers = {'x-api-key': self.api_key} if self.api_key is not None else {}
        
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
        
        if self._session is None:
            self._session = aiohttp.ClientSession()

        return await try_json(await self._session.request(method, _get_url(route), headers=headers, **kwargs))

    get = partialmethod(request, 'GET')
    post = partialmethod(request, 'POST')
    delete = partialmethod(request, 'DELETE')

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.close()
    
    async def close(self):
        if self._session is not None:
            await self._session.close()

    async def get_breeds(
        self,
        attach_breed: Optional[int] = None,
        page: Optional[int] = None, 
        limit: Optional[int] = None
    ) -> List[Breed]:
        params = {}

        if attach_breed is not None:
            params['attach_breed'] = attach_breed
        if page is not None:
            params['page'] = page
        if limit is not None:
            params['limit'] = limit

        breeds = await self.get('/breeds')
        return [Breed._from_data(self, breed) for breed in breeds]

    async def search_breeds(self, query: str) -> List[Breed]:
        breeds = await self.get('/breeds/search', params={'q': query})
        return [Breed._from_data(self, breed) for breed in breeds]

    async def get_categories(self, limit: Optional[int] = None, page: Optional[int] = None) -> List[Category]:
        params = {}

        if limit is not None:
            params['limit'] = limit
        if page is not None:
            params['page'] = page

        categories = await self.get('/categories', params=params)

        return [Category._from_data(self, category) for category in categories]
    
    async def get_votes(
        self,
        sub_id: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None
    ) -> List[Vote]:
        params = {}

        if sub_id is not None:
            params['sub_id'] = sub_id
        
        if limit is not None:
            params['limit'] = limit
        
        if page is not None:
            params['page'] = page
        
        votes = await self.get('/votes', params=params)

        return [Vote._from_data(self, vote) for vote in votes]
    
    async def create_vote(self, image_id: int, value: int, *, sub_id: Optional[str] = None) -> Vote:
        payload = {'image_id': image_id, 'value': value}

        if sub_id is not None:
            payload['sub_id'] = sub_id

        vote = await self.post('/votes', json=payload)
        return Vote._from_data(self, vote)
    
    async def get_vote(self, vote: Union[int, Vote]) -> Vote:
        vote_data = await self.get(f'/votes/{getattr(vote, "id", vote)}')
        return Vote._from_data(self, vote_data)
    
    async def delete_vote(self, vote: Union[int, Vote]) -> Dict[str, str]:
        return await self.delete(f'/votes/{getattr(vote, "id", vote)}')
    
    async def get_favourites(self, sub_id: Optional[str], limit: Optional[int], page: Optional[int]) -> List[Favourite]:
        params = {}
        if sub_id is not None:
            params['sub_id'] = sub_id
        
        if limit is not None:
            params['limit'] = limit
        
        if page is not None:
            params['page'] = page
    
        favourites = await self.get('/favourites', params=params)

        return [Favourite._from_data(self, favourite) for favourite in favourites]
    
    async def get_favourite(self, favourite_id: int) -> Favourite:
        favourite = await self.get(f'/favourites/{favourite_id}')
        return Favourite._from_data(self, favourite)

    async def delete_favourite(self, favourite: Union[int, Favourite]) -> Dict[str, str]:
        return await self.delete(f'/favourites/{getattr(favourite, "id", favourite)}')
    
    async def create_favourite(self, image_id: int, sub_id: Optional[str]) -> Favourite:
        payload = {'image_id': image_id}

        if sub_id is not None:
            payload['sub_id'] = sub_id
        
        favourite = await self.post('/favourites', json=payload)

        return Favourite._from_data(self, favourite)
    
    async def get_images(
        self,
        *,
        size: Optional[str] = None, 
        mime_types: Optional[List[str]] = None,
        order: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        category_ids: Optional[List[int]] = None,
        breed_id: Optional[int] = None,
        me: bool = False
    ) -> List[PartialImage]:
        params = {}

        if size is not None:
            params['size'] = size
        if mime_types is not None:
            params['mime_types'] = mime_types
        if order is not None:
            params['order'] = order
        if limit is not None:
            params['limit'] = limit
        if page is not None:
            params['page'] = page
        if category_ids is not None:
            params['category_ids'] = category_ids
        if breed_id is not None:
            params['breed_id'] = breed_id

        if me:
            images = await self.get('/images')
            return [Image._from_data(self, image) for image in images]

        images = await self.get('/images/search', params=params)
        return [PartialImage._from_data(self, image) for image in images]


    async def get_own_images(self, **kwargs) -> List[Image]:
        kwargs.update(me=True)
        return await self.get_images(**kwargs)
    
    # TODO: upload_image

    async def get_image(self, image_id: int):
        image = await self.get(f'/images/{image_id}')
        method = Image._from_data if "created_at" in image else PartialImage._from_data
        return method(self, image)
    
    async def delete_image(self, image_id: int) -> Dict[str, str]:
        return await self.delete(f'/images/{image_id}')

    async def get_image_analysis(self, image_id: int) -> ImageAnalysis:
        analysis = await self.get(f'/images/{image_id}/analysis')
        return ImageAnalysis._from_data(self, analysis)
