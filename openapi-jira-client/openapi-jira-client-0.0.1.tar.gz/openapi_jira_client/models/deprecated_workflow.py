from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.scope import Scope
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeprecatedWorkflow")


@attr.s(auto_attribs=True)
class DeprecatedWorkflow:
    """ Details about a workflow. """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    last_modified_date: Union[Unset, str] = UNSET
    last_modified_user: Union[Unset, str] = UNSET
    last_modified_user_account_id: Union[Unset, str] = UNSET
    steps: Union[Unset, int] = UNSET
    scope: Union[Unset, Scope] = UNSET
    default: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        last_modified_date = self.last_modified_date
        last_modified_user = self.last_modified_user
        last_modified_user_account_id = self.last_modified_user_account_id
        steps = self.steps
        scope: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.to_dict()

        default = self.default

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if last_modified_date is not UNSET:
            field_dict["lastModifiedDate"] = last_modified_date
        if last_modified_user is not UNSET:
            field_dict["lastModifiedUser"] = last_modified_user
        if last_modified_user_account_id is not UNSET:
            field_dict["lastModifiedUserAccountId"] = last_modified_user_account_id
        if steps is not UNSET:
            field_dict["steps"] = steps
        if scope is not UNSET:
            field_dict["scope"] = scope
        if default is not UNSET:
            field_dict["default"] = default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        last_modified_date = d.pop("lastModifiedDate", UNSET)

        last_modified_user = d.pop("lastModifiedUser", UNSET)

        last_modified_user_account_id = d.pop("lastModifiedUserAccountId", UNSET)

        steps = d.pop("steps", UNSET)

        scope: Union[Unset, Scope] = UNSET
        _scope = d.pop("scope", UNSET)
        if not isinstance(_scope, Unset):
            scope = Scope.from_dict(_scope)

        default = d.pop("default", UNSET)

        deprecated_workflow = cls(
            name=name,
            description=description,
            last_modified_date=last_modified_date,
            last_modified_user=last_modified_user,
            last_modified_user_account_id=last_modified_user_account_id,
            steps=steps,
            scope=scope,
            default=default,
        )

        return deprecated_workflow
