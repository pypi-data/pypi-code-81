from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.avatar_urls_bean import AvatarUrlsBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserDetails")


@attr.s(auto_attribs=True)
class UserDetails:
    """User details permitted by the user's Atlassian Account privacy settings. However, be aware of these exceptions:

    *  User record deleted from Atlassian: This occurs as the result of a right to be forgotten request. In this case, `displayName` provides an indication and other parameters have default values or are blank (for example, email is blank).
    *  User record corrupted: This occurs as a results of events such as a server import and can only happen to deleted users. In this case, `accountId` returns *unknown* and all other parameters have fallback values.
    *  User record unavailable: This usually occurs due to an internal service outage. In this case, all parameters have fallback values."""

    self_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    account_id: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    avatar_urls: Union[Unset, AvatarUrlsBean] = UNSET
    display_name: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    time_zone: Union[Unset, str] = UNSET
    account_type: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        name = self.name
        key = self.key
        account_id = self.account_id
        email_address = self.email_address
        avatar_urls: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.avatar_urls, Unset):
            avatar_urls = self.avatar_urls.to_dict()

        display_name = self.display_name
        active = self.active
        time_zone = self.time_zone
        account_type = self.account_type

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if name is not UNSET:
            field_dict["name"] = name
        if key is not UNSET:
            field_dict["key"] = key
        if account_id is not UNSET:
            field_dict["accountId"] = account_id
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address
        if avatar_urls is not UNSET:
            field_dict["avatarUrls"] = avatar_urls
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if active is not UNSET:
            field_dict["active"] = active
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone
        if account_type is not UNSET:
            field_dict["accountType"] = account_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        name = d.pop("name", UNSET)

        key = d.pop("key", UNSET)

        account_id = d.pop("accountId", UNSET)

        email_address = d.pop("emailAddress", UNSET)

        avatar_urls: Union[Unset, AvatarUrlsBean] = UNSET
        _avatar_urls = d.pop("avatarUrls", UNSET)
        if not isinstance(_avatar_urls, Unset):
            avatar_urls = AvatarUrlsBean.from_dict(_avatar_urls)

        display_name = d.pop("displayName", UNSET)

        active = d.pop("active", UNSET)

        time_zone = d.pop("timeZone", UNSET)

        account_type = d.pop("accountType", UNSET)

        user_details = cls(
            self_=self_,
            name=name,
            key=key,
            account_id=account_id,
            email_address=email_address,
            avatar_urls=avatar_urls,
            display_name=display_name,
            active=active,
            time_zone=time_zone,
            account_type=account_type,
        )

        return user_details
