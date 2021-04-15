from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.user import User
from ..types import UNSET, Unset

T = TypeVar("T", bound="Votes")


@attr.s(auto_attribs=True)
class Votes:
    """ The details of votes on an issue. """

    self_: Union[Unset, str] = UNSET
    votes: Union[Unset, int] = UNSET
    has_voted: Union[Unset, bool] = UNSET
    voters: Union[Unset, List[User]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        votes = self.votes
        has_voted = self.has_voted
        voters: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.voters, Unset):
            voters = []
            for voters_item_data in self.voters:
                voters_item = voters_item_data.to_dict()

                voters.append(voters_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if votes is not UNSET:
            field_dict["votes"] = votes
        if has_voted is not UNSET:
            field_dict["hasVoted"] = has_voted
        if voters is not UNSET:
            field_dict["voters"] = voters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        votes = d.pop("votes", UNSET)

        has_voted = d.pop("hasVoted", UNSET)

        voters = []
        _voters = d.pop("voters", UNSET)
        for voters_item_data in _voters or []:
            voters_item = User.from_dict(voters_item_data)

            voters.append(voters_item)

        votes = cls(
            self_=self_,
            votes=votes,
            has_voted=has_voted,
            voters=voters,
        )

        return votes
