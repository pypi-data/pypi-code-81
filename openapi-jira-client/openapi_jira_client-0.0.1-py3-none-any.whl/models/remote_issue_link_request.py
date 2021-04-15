from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.application import Application
from ..models.remote_object import RemoteObject
from ..types import UNSET, Unset

T = TypeVar("T", bound="RemoteIssueLinkRequest")


@attr.s(auto_attribs=True)
class RemoteIssueLinkRequest:
    """ Details of a remote issue link. """

    object_: RemoteObject
    global_id: Union[Unset, str] = UNSET
    application: Union[Unset, Application] = UNSET
    relationship: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.to_dict()

        global_id = self.global_id
        application: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.application, Unset):
            application = self.application.to_dict()

        relationship = self.relationship

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
            }
        )
        if global_id is not UNSET:
            field_dict["globalId"] = global_id
        if application is not UNSET:
            field_dict["application"] = application
        if relationship is not UNSET:
            field_dict["relationship"] = relationship

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = RemoteObject.from_dict(d.pop("object"))

        global_id = d.pop("globalId", UNSET)

        application: Union[Unset, Application] = UNSET
        _application = d.pop("application", UNSET)
        if not isinstance(_application, Unset):
            application = Application.from_dict(_application)

        relationship = d.pop("relationship", UNSET)

        remote_issue_link_request = cls(
            object_=object_,
            global_id=global_id,
            application=application,
            relationship=relationship,
        )

        remote_issue_link_request.additional_properties = d
        return remote_issue_link_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
