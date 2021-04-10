__all__ = ('Client',)

import requests
from json import JSONDecodeError
from functools import partialmethod
from typing import Dict, List, Optional, Union

from .models import Breed, Category, Favourite, Image, ImageAnalysis, PartialImage, Vote

RequestResponse = Union[dict, str]

BASE_API_URL = 'https://api.thedogapi.com/v1'

def try_json(response: requests.Response) -> RequestResponse:
    response.raise_for_status()
    try:
        return response.json()
    except JSONDecodeError:
        return response.text

def _get_url(route: str):
    return BASE_API_URL + route

class Client:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key
    
    def request(self, method: str, route: str, **kwargs) -> RequestResponse:
        headers = {'x-api-key': self.api_key} if self.api_key is not None else {}

        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))

        return try_json(requests.request(method, _get_url(route), headers=headers, **kwargs))
    
    get = partialmethod(request, 'GET')
    post = partialmethod(request, 'POST')
    delete = partialmethod(request, 'DELETE')

    def get_breeds(
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

        breeds = self.get('/breeds')
        return [Breed._from_data(self, breed) for breed in breeds]

    def search_breeds(self, query: str) -> List[Breed]:
        breeds = self.get('/breeds/search', params={'q': query})
        return [Breed._from_data(self, breed) for breed in breeds]

    def get_categories(self, limit: Optional[int] = None, page: Optional[int] = None) -> List[Category]:
        params = {}

        if limit is not None:
            params['limit'] = limit
        if page is not None:
            params['page'] = page

        categories = self.get('/categories', params=params)

        return [Category._from_data(self, category) for category in categories] 
        # For some reason, the api may return no categories.

    def get_votes(
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
        
        votes = self.get('/votes', params=params)

        return [Vote._from_data(self, vote) for vote in votes]
    
    def create_vote(self, image_id: int, value: int, *, sub_id: Optional[str] = None) -> Vote:
        payload = {'image_id': image_id, 'value': value}

        if sub_id is not None:
            payload['sub_id'] = sub_id

        vote = self.post('/votes', json=payload)
        return Vote._from_data(self, vote)
    
    def get_vote(self, vote: Union[int, Vote]) -> Vote:
        vote_data = self.get(f'/votes/{getattr(vote, "id", vote)}')
        return Vote._from_data(self, vote_data)
    
    def delete_vote(self, vote: Union[int, Vote]) -> Dict[str, str]:
        return self.delete(f'/votes/{getattr(vote, "id", vote)}')
    
    def get_favourites(self, sub_id: Optional[str], limit: Optional[int], page: Optional[int]) -> List[Favourite]:
        params = {}
        if sub_id is not None:
            params['sub_id'] = sub_id
        
        if limit is not None:
            params['limit'] = limit
        
        if page is not None:
            params['page'] = page
    
        favourites = self.get('/favourites', params=params)

        return [Favourite._from_data(self, favourite) for favourite in favourites]
    
    def get_favourite(self, favourite_id: int) -> Favourite:
        favourite = self.get(f'/favourites/{favourite_id}')
        return Favourite._from_data(self, favourite)

    def delete_favourite(self, favourite: Union[int, Favourite]) -> Dict[str, str]:
        return self.delete(f'/favourites/{getattr(favourite, "id", favourite)}')
    
    def create_favourite(self, image_id: int, sub_id: Optional[str]) -> Favourite:
        payload = {'image_id': image_id}

        if sub_id is not None:
            payload['sub_id'] = sub_id
        
        favourite  = self.post('/favourites', json=payload)

        return Favourite._from_data(self, favourite)
    
    def get_images(
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
            images = self.get('/images')
            return [Image._from_data(self, image) for image in images]
        images = self.get('/images/search', params=params)
        return [PartialImage._from_data(self, image) for image in images]


    def get_own_images(self, **kwargs) -> List[Image]:
        kwargs.update(me=True)
        return self.get_images(**kwargs)
    
    # TODO: upload_image

    def get_image(self, image_id: int):
        image = self.get(f'/images/{image_id}')
        method = Image._from_data if "created_at" in image else PartialImage._from_data
        return method(self, image)
    
    def delete_image(self, image_id: int) -> Dict[str, str]:
        return self.delete(f'/images/{image_id}')

    def get_image_analysis(self, image_id: int) -> ImageAnalysis:
        analysis = self.get(f'/images/{image_id}/analysis')
        return ImageAnalysis._from_data(self, analysis)
