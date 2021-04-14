from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.naming_strategy import NamingStrategy
from ..types import UNSET, Unset

T = TypeVar("T", bound="BioentityRegistrationFields")


@attr.s(auto_attribs=True)
class BioentityRegistrationFields:
    """  """

    entity_registry_id: Union[Unset, str] = UNSET
    naming_strategy: Union[Unset, NamingStrategy] = UNSET
    registry_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        entity_registry_id = self.entity_registry_id
        naming_strategy: Union[Unset, int] = UNSET
        if not isinstance(self.naming_strategy, Unset):
            naming_strategy = self.naming_strategy.value

        registry_id = self.registry_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if entity_registry_id is not UNSET:
            field_dict["entityRegistryId"] = entity_registry_id
        if naming_strategy is not UNSET:
            field_dict["namingStrategy"] = naming_strategy
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_registry_id = d.pop("entityRegistryId", UNSET)

        naming_strategy = None
        _naming_strategy = d.pop("namingStrategy", UNSET)
        if _naming_strategy is not None and _naming_strategy is not UNSET:
            naming_strategy = NamingStrategy(_naming_strategy)

        registry_id = d.pop("registryId", UNSET)

        bioentity_registration_fields = cls(
            entity_registry_id=entity_registry_id,
            naming_strategy=naming_strategy,
            registry_id=registry_id,
        )

        return bioentity_registration_fields
