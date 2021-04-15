from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="HealthCheckResult")


@attr.s(auto_attribs=True)
class HealthCheckResult:
    """ Jira instance health check results. Deprecated and no longer returned. """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    passed: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        passed = self.passed

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if passed is not UNSET:
            field_dict["passed"] = passed

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        passed = d.pop("passed", UNSET)

        health_check_result = cls(
            name=name,
            description=description,
            passed=passed,
        )

        return health_check_result
