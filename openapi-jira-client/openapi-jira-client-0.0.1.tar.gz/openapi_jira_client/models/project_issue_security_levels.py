from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.security_level import SecurityLevel

T = TypeVar("T", bound="ProjectIssueSecurityLevels")


@attr.s(auto_attribs=True)
class ProjectIssueSecurityLevels:
    """ List of issue level security items in a project. """

    levels: List[SecurityLevel]

    def to_dict(self) -> Dict[str, Any]:
        levels = []
        for levels_item_data in self.levels:
            levels_item = levels_item_data.to_dict()

            levels.append(levels_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "levels": levels,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        levels = []
        _levels = d.pop("levels")
        for levels_item_data in _levels:
            levels_item = SecurityLevel.from_dict(levels_item_data)

            levels.append(levels_item)

        project_issue_security_levels = cls(
            levels=levels,
        )

        return project_issue_security_levels
