from typing import Union, List

import time
from tqdm import tqdm

from .enums import ModelType
from .feature import Feature, FeatureList
from pyrasgo.connection import Connection
from pyrasgo.monitoring import track_usage
from pyrasgo.schemas.attributes import Attribute, CollectionAttributes, CollectionAttributeBulkCreate
from pyrasgo.schemas import collection as api


class Collection(Connection):
    """
    Stores a Rasgo Collection
    """

    def __init__(self, api_object, **kwargs):
        super().__init__(**kwargs)
        self._fields = api.Collection(**api_object)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Collection(id={self.id}, name={self.name}, type={self.modelType.name}, authorId={self.authorId}, isShared={self.isShared})"

    def __getattr__(self, item):
        try:
            return self._fields.__getattribute__(item)
        except KeyError:
            self.get()
        try:
            return self._fields.__getattribute__(item)
        except KeyError:
            raise AttributeError(f"No attribute named {item}")

    @property
    @track_usage
    def modelType(self):
        """
        Returns the type of the Collection
        """
        return ModelType(self._fields.type)

    @property
    def features(self):
        """
        Returns the Features within the Collection
        """
        try:
            return FeatureList([feature.dict() for feature in self._fields.features])
        except AttributeError:
            self.get()
        return FeatureList([feature.dict() for feature in self._fields.features])

    @features.setter
    def features(self, features: Union[List[Feature], FeatureList, Feature]):
        # Update the namespace
        self._fields.__setattr__('features',
                                    [Feature(api_object=feature.dict()) for feature in self.features + features])

    @track_usage
    def get(self):
        """
        Updates the Collection's attributes from the API
        """
        self._fields = Feature(api_object=self._get(f"/models/{self.id}", api_version=1).json())

    @track_usage
    def get_author(self):
        """
        Returns the author object of the Collection (includes credentials if user is author)
        """
        if self._profile['id'] == self.authorId:
            author = self._profile
        else:
            author = self._get(f"/users/{self.authorId}", api_version=1).json()
        return f'Author({author["id"]}, {author["firstName"]} {author["lastName"]})'

    @track_usage
    def rename(self, new_name: str):
        """
        Updates a Collection's display name
        """
        print(f"Renaming Collection {self.id} from {self.name} to {new_name}")
        collection = api.CollectionUpdate(id=self.id, name=new_name)
        self._fields = api.Collection(**self._patch(f"/models/{self.id}/details", 
                                                    api_version=1, _json=collection.dict(exclude_unset=True, exclude_none=True)).json())

    @track_usage
    def share(self, share: bool=True) -> bool:
        """
        Share the Collection with your organization
        :param share: True to make your Collection public. False to make your Collection private
        """
        response = self._patch(f"/models/{self.id}/details", api_version=1, _json={"isShared": share}).json()
        return response['isShared']

    @track_usage
    def add_feature(self, feature: Feature) -> None:
        """
        Adds a single feature to the Collection
        """
        self.features = feature
        self._patch(f"/models/{self.id}/features", api_version=1,
                    _json={"featureIds": [str(feature.id)]})

    @track_usage
    def add_features(self, features: Union[List[Feature], FeatureList]) -> None:
        """
        Adds a FeatureList or a list of Features to the Collection
        """
        self.features = features
        self._patch(f"/models/{self.id}/features", api_version=1,
                    _json={"featureIds": [str(feature.id) for feature in features]})

    @track_usage
    def is_data_ready(self) -> bool:
        """
        Performs check against API for training data readiness, if true, a dataframe can be pulled down.
        :return:
        """
        r = self._get("/trainings/latest", api_version=0)
        if any([model['state'] == 'done' for model in r.json() if model['model']['id'] == self.id]):
            return True
        if any([model['state'] == 'error' for model in r.json() if model['model']['id'] == self.id]):
            raise SystemError("There's been an issue with the training data generation")
        return False

    @track_usage
    def generate_training_data(self) -> None:
        """
        Triggers the generation of the Collection's training data.
        """
        self._post(f"/trainings/", _json={"modelId": int(self.id),
                                          "userId": self._profile['id']},
                   api_version=0)
        for _ in tqdm(range(0, 10), leave=False):
            if self.is_data_ready():
                break
            time.sleep(1)

    @track_usage
    def add_attributes(self, attributes: List[dict]):
        if not isinstance(attributes, list):
            raise ValueError('attributes parameter must be passed in as a list of k:v pairs. Example: [{"key": "value"}, {"key": "value"}]')
        attr = []
        for kv in attributes:
            if not isinstance(kv, dict):
                raise ValueError('attributes parameter must be passed in as a list of k:v pairs. Example: [{"key": "value"}, {"key": "value"}]')
            for k, v in kv.items():
                attr.append(Attribute(key=k, value=v))
        attr_in = CollectionAttributeBulkCreate(collectionId = self.id, attributes=attr)
        return self._put(f"/models/{self.id}/attributes", attr_in.dict(exclude_unset=True), api_version=1).json()

    @property
    @track_usage
    def attributes(self) -> dict:
        """
        Helper property to convert a list of dicts into a single dict
        """
        attr_dict = {}
        response = self._get(f"/models/{self.id}/attributes", api_version=1).json()
        for a in response:
            attr_dict.update({a['key']: a['value']})
        return attr_dict

    def _make_table_metadata(self):
        organization = self._get_profile().get("organization")
        metadata = {
            "database": organization.get("database"),
            "schema": organization.get("schema"),
            "table": self._fields.dataTableName,
        }
        return metadata