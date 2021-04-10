from __future__ import annotations

__all__ = ('BaseObject', 'Weight', 'Height', 'Model', 'Breed', 'Category')

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

def get_slots(cls: type) -> List[str]:
    lst = []
    for class_ in cls.mro():
        if hasattr(class_, '__slots__'):
            lst.extend(class_.__slots__)
    return lst


class BaseObject:
    __slots__ = ()

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> BaseObject:
        return cls(**{name: data.get(name) for name in get_slots(cls) if not name.startswith('_')})
    
    def __repr__(self) -> str:
        string = f'<{self.__class__.__name__} '
        lst = []
        for slot in get_slots(self.__class__):
            value = getattr(self, slot, None)
            if value is not None and not slot.startswith('_'):
                lst.append(f'{slot}={value!r}')
        return string + ', '.join(lst) + '>'


class Weight(BaseObject):
    __slots__ = ('imperial', 'metric')
    
    def __init__(self, imperial: str, metric: str) -> None:
        self.imperial = imperial
        self.metric = metric

class Height(BaseObject):
    __slots__ = ('imperial', 'metric')
    
    def __init__(self, imperial: str, metric: str) -> None:
        self.imperial = imperial
        self.metric = metric

class Model(BaseObject):
    __slots__ = ('id', '_client')

    def __init__(self, id: Union[int, str]) -> None:
        if id is None:
            raise ValueError("You must pass an non-none `id` to __init__")
        self.id = id

    @classmethod
    def _from_data(cls, client, data: Dict[str, Any]) -> Model:
        self = super()._from_data(data)
        self._client = client
        return self

class Breed(Model):
    __slots__ = ('name', 'temperament', 'life_span', 'alt_names', 'origin', 'weight',
                'country_code', 'height', 'description', 'image', 'reference_image_id',
                'breed_group', 'bred_for', 'history')

    def __init__(
        self,
        id: int,
        name: str,
        reference_image_id: str,
        weight: Weight,
        height: Height,
        image: Model,
        life_span: str,
        alt_names: Optional[str] = None,
        temperament: Optional[str] = None,
        origin: Optional[str] = None,
        country_code: Optional[str] = None,
        description: Optional[str] = None,
        breed_group: Optional[str] = None,
        bred_for: Optional[str] = None,
        history: Optional[str] = None
    ) -> None:
        super().__init__(id)
        self.name = name
        self.temperament = temperament
        self.life_span = life_span
        self.origin = origin
        self.weight = Weight._from_data(weight)
        self.country_code = country_code
        self.height = Height._from_data(height)
        self.description = description
        self.image = image
        self.reference_image_id = reference_image_id
        self.breed_group = breed_group
        self.bred_for = bred_for
        self.history = history
        self.alt_names = alt_names
    
    @property
    def temperaments(self) -> Optional[List[str]]:
        return self.temperament and self.temperament.split(', ')

class Category(Model):
    __slots__ = ('name',)

    def __init__(self, id: int, name: str) -> None:
        super().__init__(id)
        self.name = name

class Fact(Model):
    __slots__ = ('text', 'language_code', 'breed_id')

    def __init__(self, id: int, text: str, breed_id: int) -> None:
        super().__init__(id)
        self.text = text
        self.breed_id = breed_id
    
class Favourite(Model):
    __slots__ = ('image_id', 'sub_id', 'created_at')

    def __init__(self, id: int, image_id: int, sub_id: int, created_at: str) -> None:
        super().__init__(id)
        self.image_id = image_id
        self.sub_id = sub_id
        self.created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.000Z')

    def delete(self):
        return self._client.delete_favourite(self.id)

class Vote(Model):
    __slots__ = ('value', 'image_id', 'sub_id', 'created_at', 'country_code')

    def __init__(
        self,
        id: Optional[int],
        value: int,
        image_id: int,
        sub_id: Optional[int],
        created_at: Optional[str],
        country_code: Optional[str]
    ) -> None:
        super().__init__(id)
        self.image_id = image_id
        self.sub_id = sub_id
        self.created_at = None
        if created_at is not None:
            self.created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.000Z")
        self.country_code = country_code
        self.value = value

    def delete(self):
        return self._client.delete_vote(self.id)

class PartialImage(Model):
    __slots__ = ('url', 'categories', 'breeds')

    def __init__(
        self,
        id: int,
        url: str,
        categories: List[Dict[str, Union[str, int]]],
        breeds: List[Dict[str, Union[str, dict]]]) -> None:
        super().__init__(id)
        self.url = url
        self.categories = self.breeds = None
        if categories is not None:
            self.categories = [Category._from_data(None, category) for category in categories]
        if breeds is not None:
            self.breeds = [Breed._from_data(None, breed) for breed in breeds]

    def delete(self) -> Dict[str, str]:
        return self._client.delete_vote(self)
    
    def get_analysis(self) -> ImageAnalysis:
        return self._client.get_image_analysis(self)
    
    def favourite(self, sub_id: Optional[str] = None) -> Favourite:
        return self._client.create_favourite(self.id, sub_id)
    
    def vote(self, value: int, sub_id: Optional[str] = None):
        return self._client.create_vote(self.id, value, sub_id)

class Image(PartialImage):
    __slots__ = ('sub_id', 'created_at', 'original_filename')

    def __init__(
        self,
        id: int,
        url: str,
        categories: Optional[List[Dict[str, Union[str, int]]]],
        breeds: Optional[List[Dict[str, Union[str, dict]]]],
        sub_id: str,
        created_at: str,
        original_filename: str
    ) -> None:
        super().__init__(id, url, categories, breeds)
        self.sub_id = sub_id
        self.created_at = None
        if created_at is not None:
            self.created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.000Z')
        self.original_filename = original_filename

class ImageAnalysis(Model):
    __slots__ = ('labels', 'moderation_labels', 'vendor', 'approved', 'rejected')

    def __init__(
        self,
        id: int,
        labels: List[Dict[str, Any]],
        moderation_labels: List[Dict[str, Any]],
        vendor: str,
        approved: int,
        rejected: int
    ) -> None:
        super().__init__(id)
        self.labels = labels
        self.moderation_labels = moderation_labels
        self.vendor = vendor
        self.approved = bool(approved)
        self.rejected = bool(rejected)

class Source(Model):
    __slots__ = ('name', 'website_url', 'breed_id')
    def __init__(self, id: int, name: str, website_url: str, breed_id: Optional[int]) -> None:
        super().__init__(id)
        self.name = name
        self.website_url = website_url
        self.breed_id = breed_id
    