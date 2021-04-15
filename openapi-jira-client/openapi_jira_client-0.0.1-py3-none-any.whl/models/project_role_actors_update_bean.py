from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_project_role_actors_update_bean_categorised_actors import (
    ComponentsschemasProjectRoleActorsUpdateBeanCategorisedActors,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectRoleActorsUpdateBean")


@attr.s(auto_attribs=True)
class ProjectRoleActorsUpdateBean:
    """  """

    id_: Union[Unset, int] = UNSET
    categorised_actors: Union[Unset, ComponentsschemasProjectRoleActorsUpdateBeanCategorisedActors] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        categorised_actors: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.categorised_actors, Unset):
            categorised_actors = self.categorised_actors.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if categorised_actors is not UNSET:
            field_dict["categorisedActors"] = categorised_actors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        categorised_actors: Union[Unset, ComponentsschemasProjectRoleActorsUpdateBeanCategorisedActors] = UNSET
        _categorised_actors = d.pop("categorisedActors", UNSET)
        if not isinstance(_categorised_actors, Unset):
            categorised_actors = ComponentsschemasProjectRoleActorsUpdateBeanCategorisedActors.from_dict(
                _categorised_actors
            )

        project_role_actors_update_bean = cls(
            id_=id_,
            categorised_actors=categorised_actors,
        )

        return project_role_actors_update_bean
