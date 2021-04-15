from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="ComponentsschemasProjectRoleActorsUpdateBeanCategorisedActors")


@attr.s(auto_attribs=True)
class ComponentsschemasProjectRoleActorsUpdateBeanCategorisedActors:
    """ The actors to add to the project role. Add groups using `atlassian-group-role-actor` and a list of group names. For example, `"atlassian-group-role-actor":["another","administrators"]}`. Add users using `atlassian-user-role-actor` and a list of account IDs. For example, `"atlassian-user-role-actor":["12345678-9abc-def1-2345-6789abcdef12", "abcdef12-3456-789a-bcde-f123456789ab"]`. """

    additional_properties: Dict[str, List[str]] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        componentsschemas_project_role_actors_update_bean_categorised_actors = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = cast(List[str], prop_dict)

            additional_properties[prop_name] = additional_property

        componentsschemas_project_role_actors_update_bean_categorised_actors.additional_properties = (
            additional_properties
        )
        return componentsschemas_project_role_actors_update_bean_categorised_actors

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> List[str]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: List[str]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
