import json
import logging
from dataclasses import dataclass
from typing import Dict, List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from smart_open import open

from metaphor.common.event_util import EventUtil
from metaphor.common.extractor import BaseExtractor, RunConfig
from metaphor.common.metadata_change_event import (
    EntityType,
    Group,
    GroupID,
    GroupInfo,
    MetadataChangeEvent,
    Person,
    PersonID,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user",
    "https://www.googleapis.com/auth/admin.directory.group",
]


class InvalidTokenError(Exception):
    """Thrown when the OAuth token is no longer valid"""

    def __init__(self):
        super.__init__(self, "Token is no longer valid. Please authenticate again")


@dataclass
class GoogleDirectoryRunConfig(RunConfig):
    user_info: dict

    @classmethod
    def from_json_file(cls, path: str) -> "RunConfig":
        with open(path, encoding="utf8") as fin:
            return GoogleDirectoryRunConfig(json.load(fin))


class GoogleDirectoryExtractor(BaseExtractor):
    """Google Directory metadata extractor"""

    def __init__(self):
        self._users: List[Person] = []
        self._groups: List[Group] = []

    async def extract(self, config: RunConfig) -> List[MetadataChangeEvent]:
        assert isinstance(config, GoogleDirectoryRunConfig)

        logger.info("Fetching metadata from Google Directory")

        service = self._get_directory_service(config)

        # get all users
        results = (
            service.users().list(customer="my_customer", orderBy="email").execute()
        )
        users = results.get("users", [])

        for user in users:
            self._parse_user(user)

        # get all groups
        results = (
            service.groups().list(customer="my_customer", orderBy="email").execute()
        )
        groups = results.get("groups", [])

        for group in groups:
            # get group members
            response = (
                service.members()
                .list(groupKey=group["email"], includeDerivedMembership=True)
                .execute()
            )
            members = response["members"]

            self._parse_group(group, members)

        logger.debug(json.dumps([p.to_dict() for p in self._users]))
        logger.debug(json.dumps([p.to_dict() for p in self._groups]))

        return [EventUtil.build_person_event(p) for p in self._users] + [
            EventUtil.build_group_event(p) for p in self._groups
        ]

    @staticmethod
    def _get_directory_service(config: GoogleDirectoryRunConfig):
        credential = Credentials.from_authorized_user_info(config.user_info, SCOPES)
        # If token expired, try refresh it.
        if not credential.valid:
            if credential.expired and credential.refresh_token:
                credential.refresh(Request())
            else:
                raise InvalidTokenError()

        return build("admin", "directory_v1", credentials=credential)

    def _parse_user(self, user: Dict) -> None:
        person = Person()
        person.entity_type = EntityType.PERSON
        person.logical_id = PersonID()
        person.logical_id.email = user["primaryEmail"]
        person.first_name = user["name"]["givenName"]
        person.last_name = user["name"]["familyName"]
        if "thumbnailPhotoUrl" in user:
            person.avatar_url = user["thumbnailPhotoUrl"]

        self._users.append(person)

    def _parse_group(self, group: Dict, members: List[Dict]) -> None:
        grp = Group()
        grp.entity_type = EntityType.GROUP
        grp.logical_id = GroupID()
        grp.logical_id.group_name = group["name"]
        grp.group_info = GroupInfo()
        grp.group_info.email = group["email"]
        grp.group_info.admins = []
        grp.group_info.members = []
        grp.group_info.subgroups = []

        for member in members:
            # TODO: get subgroups instead of derived members
            if member["type"] == "USER":
                user = PersonID()
                user.email = member["email"]

                if member["role"] in ["OWNER", "MANAGER"]:
                    grp.group_info.admins.append(user)
                else:
                    grp.group_info.members.append(user)

        self._groups.append(grp)
