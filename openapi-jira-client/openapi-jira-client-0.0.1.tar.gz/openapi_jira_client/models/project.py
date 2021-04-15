import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.avatar_urls_bean import AvatarUrlsBean
from ..models.component import Component
from ..models.componentsschemas_project_assignee_type import ComponentsschemasProjectAssigneeType
from ..models.componentsschemas_project_project_type_key import ComponentsschemasProjectProjectTypeKey
from ..models.componentsschemas_project_properties import ComponentsschemasProjectProperties
from ..models.componentsschemas_project_roles import ComponentsschemasProjectRoles
from ..models.componentsschemas_project_style import ComponentsschemasProjectStyle
from ..models.hierarchy import Hierarchy
from ..models.issue_type_details import IssueTypeDetails
from ..models.project_category import ProjectCategory
from ..models.project_insight import ProjectInsight
from ..models.project_permissions import ProjectPermissions
from ..models.user import User
from ..models.version import Version
from ..types import UNSET, Unset

T = TypeVar("T", bound="Project")


@attr.s(auto_attribs=True)
class Project:
    """ Details about a project. """

    expand: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    lead: Union[Unset, User] = UNSET
    components: Union[Unset, List[Component]] = UNSET
    issue_types: Union[Unset, List[IssueTypeDetails]] = UNSET
    url: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    assignee_type: Union[Unset, ComponentsschemasProjectAssigneeType] = UNSET
    versions: Union[Unset, List[Version]] = UNSET
    name: Union[Unset, str] = UNSET
    roles: Union[Unset, ComponentsschemasProjectRoles] = UNSET
    avatar_urls: Union[Unset, AvatarUrlsBean] = UNSET
    project_category: Union[Unset, ProjectCategory] = UNSET
    project_type_key: Union[Unset, ComponentsschemasProjectProjectTypeKey] = UNSET
    simplified: Union[Unset, bool] = UNSET
    style: Union[Unset, ComponentsschemasProjectStyle] = UNSET
    favourite: Union[Unset, bool] = UNSET
    is_private: Union[Unset, bool] = UNSET
    issue_type_hierarchy: Union[Unset, Hierarchy] = UNSET
    permissions: Union[Unset, ProjectPermissions] = UNSET
    properties: Union[Unset, ComponentsschemasProjectProperties] = UNSET
    uuid: Union[Unset, str] = UNSET
    insight: Union[Unset, ProjectInsight] = UNSET
    deleted: Union[Unset, bool] = UNSET
    retention_till_date: Union[Unset, datetime.datetime] = UNSET
    deleted_date: Union[Unset, datetime.datetime] = UNSET
    deleted_by: Union[Unset, User] = UNSET
    archived: Union[Unset, bool] = UNSET
    archived_date: Union[Unset, datetime.datetime] = UNSET
    archived_by: Union[Unset, User] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expand = self.expand
        self_ = self.self_
        id_ = self.id_
        key = self.key
        description = self.description
        lead: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.lead, Unset):
            lead = self.lead.to_dict()

        components: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.components, Unset):
            components = []
            for components_item_data in self.components:
                components_item = components_item_data.to_dict()

                components.append(components_item)

        issue_types: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.issue_types, Unset):
            issue_types = []
            for issue_types_item_data in self.issue_types:
                issue_types_item = issue_types_item_data.to_dict()

                issue_types.append(issue_types_item)

        url = self.url
        email = self.email
        assignee_type: Union[Unset, str] = UNSET
        if not isinstance(self.assignee_type, Unset):
            assignee_type = self.assignee_type.value

        versions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.versions, Unset):
            versions = []
            for versions_item_data in self.versions:
                versions_item = versions_item_data.to_dict()

                versions.append(versions_item)

        name = self.name
        roles: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles.to_dict()

        avatar_urls: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.avatar_urls, Unset):
            avatar_urls = self.avatar_urls.to_dict()

        project_category: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.project_category, Unset):
            project_category = self.project_category.to_dict()

        project_type_key: Union[Unset, str] = UNSET
        if not isinstance(self.project_type_key, Unset):
            project_type_key = self.project_type_key.value

        simplified = self.simplified
        style: Union[Unset, str] = UNSET
        if not isinstance(self.style, Unset):
            style = self.style.value

        favourite = self.favourite
        is_private = self.is_private
        issue_type_hierarchy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.issue_type_hierarchy, Unset):
            issue_type_hierarchy = self.issue_type_hierarchy.to_dict()

        permissions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions.to_dict()

        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        uuid = self.uuid
        insight: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.insight, Unset):
            insight = self.insight.to_dict()

        deleted = self.deleted
        retention_till_date: Union[Unset, str] = UNSET
        if not isinstance(self.retention_till_date, Unset):
            retention_till_date = self.retention_till_date.isoformat()

        deleted_date: Union[Unset, str] = UNSET
        if not isinstance(self.deleted_date, Unset):
            deleted_date = self.deleted_date.isoformat()

        deleted_by: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.deleted_by, Unset):
            deleted_by = self.deleted_by.to_dict()

        archived = self.archived
        archived_date: Union[Unset, str] = UNSET
        if not isinstance(self.archived_date, Unset):
            archived_date = self.archived_date.isoformat()

        archived_by: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.archived_by, Unset):
            archived_by = self.archived_by.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if expand is not UNSET:
            field_dict["expand"] = expand
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id_ is not UNSET:
            field_dict["id"] = id_
        if key is not UNSET:
            field_dict["key"] = key
        if description is not UNSET:
            field_dict["description"] = description
        if lead is not UNSET:
            field_dict["lead"] = lead
        if components is not UNSET:
            field_dict["components"] = components
        if issue_types is not UNSET:
            field_dict["issueTypes"] = issue_types
        if url is not UNSET:
            field_dict["url"] = url
        if email is not UNSET:
            field_dict["email"] = email
        if assignee_type is not UNSET:
            field_dict["assigneeType"] = assignee_type
        if versions is not UNSET:
            field_dict["versions"] = versions
        if name is not UNSET:
            field_dict["name"] = name
        if roles is not UNSET:
            field_dict["roles"] = roles
        if avatar_urls is not UNSET:
            field_dict["avatarUrls"] = avatar_urls
        if project_category is not UNSET:
            field_dict["projectCategory"] = project_category
        if project_type_key is not UNSET:
            field_dict["projectTypeKey"] = project_type_key
        if simplified is not UNSET:
            field_dict["simplified"] = simplified
        if style is not UNSET:
            field_dict["style"] = style
        if favourite is not UNSET:
            field_dict["favourite"] = favourite
        if is_private is not UNSET:
            field_dict["isPrivate"] = is_private
        if issue_type_hierarchy is not UNSET:
            field_dict["issueTypeHierarchy"] = issue_type_hierarchy
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if properties is not UNSET:
            field_dict["properties"] = properties
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if insight is not UNSET:
            field_dict["insight"] = insight
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if retention_till_date is not UNSET:
            field_dict["retentionTillDate"] = retention_till_date
        if deleted_date is not UNSET:
            field_dict["deletedDate"] = deleted_date
        if deleted_by is not UNSET:
            field_dict["deletedBy"] = deleted_by
        if archived is not UNSET:
            field_dict["archived"] = archived
        if archived_date is not UNSET:
            field_dict["archivedDate"] = archived_date
        if archived_by is not UNSET:
            field_dict["archivedBy"] = archived_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expand = d.pop("expand", UNSET)

        self_ = d.pop("self", UNSET)

        id_ = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        description = d.pop("description", UNSET)

        lead: Union[Unset, User] = UNSET
        _lead = d.pop("lead", UNSET)
        if not isinstance(_lead, Unset):
            lead = User.from_dict(_lead)

        components = []
        _components = d.pop("components", UNSET)
        for components_item_data in _components or []:
            components_item = Component.from_dict(components_item_data)

            components.append(components_item)

        issue_types = []
        _issue_types = d.pop("issueTypes", UNSET)
        for issue_types_item_data in _issue_types or []:
            issue_types_item = IssueTypeDetails.from_dict(issue_types_item_data)

            issue_types.append(issue_types_item)

        url = d.pop("url", UNSET)

        email = d.pop("email", UNSET)

        assignee_type: Union[Unset, ComponentsschemasProjectAssigneeType] = UNSET
        _assignee_type = d.pop("assigneeType", UNSET)
        if not isinstance(_assignee_type, Unset):
            assignee_type = ComponentsschemasProjectAssigneeType(_assignee_type)

        versions = []
        _versions = d.pop("versions", UNSET)
        for versions_item_data in _versions or []:
            versions_item = Version.from_dict(versions_item_data)

            versions.append(versions_item)

        name = d.pop("name", UNSET)

        roles: Union[Unset, ComponentsschemasProjectRoles] = UNSET
        _roles = d.pop("roles", UNSET)
        if not isinstance(_roles, Unset):
            roles = ComponentsschemasProjectRoles.from_dict(_roles)

        avatar_urls: Union[Unset, AvatarUrlsBean] = UNSET
        _avatar_urls = d.pop("avatarUrls", UNSET)
        if not isinstance(_avatar_urls, Unset):
            avatar_urls = AvatarUrlsBean.from_dict(_avatar_urls)

        project_category: Union[Unset, ProjectCategory] = UNSET
        _project_category = d.pop("projectCategory", UNSET)
        if not isinstance(_project_category, Unset):
            project_category = ProjectCategory.from_dict(_project_category)

        project_type_key: Union[Unset, ComponentsschemasProjectProjectTypeKey] = UNSET
        _project_type_key = d.pop("projectTypeKey", UNSET)
        if not isinstance(_project_type_key, Unset):
            project_type_key = ComponentsschemasProjectProjectTypeKey(_project_type_key)

        simplified = d.pop("simplified", UNSET)

        style: Union[Unset, ComponentsschemasProjectStyle] = UNSET
        _style = d.pop("style", UNSET)
        if not isinstance(_style, Unset):
            style = ComponentsschemasProjectStyle(_style)

        favourite = d.pop("favourite", UNSET)

        is_private = d.pop("isPrivate", UNSET)

        issue_type_hierarchy: Union[Unset, Hierarchy] = UNSET
        _issue_type_hierarchy = d.pop("issueTypeHierarchy", UNSET)
        if not isinstance(_issue_type_hierarchy, Unset):
            issue_type_hierarchy = Hierarchy.from_dict(_issue_type_hierarchy)

        permissions: Union[Unset, ProjectPermissions] = UNSET
        _permissions = d.pop("permissions", UNSET)
        if not isinstance(_permissions, Unset):
            permissions = ProjectPermissions.from_dict(_permissions)

        properties: Union[Unset, ComponentsschemasProjectProperties] = UNSET
        _properties = d.pop("properties", UNSET)
        if not isinstance(_properties, Unset):
            properties = ComponentsschemasProjectProperties.from_dict(_properties)

        uuid = d.pop("uuid", UNSET)

        insight: Union[Unset, ProjectInsight] = UNSET
        _insight = d.pop("insight", UNSET)
        if not isinstance(_insight, Unset):
            insight = ProjectInsight.from_dict(_insight)

        deleted = d.pop("deleted", UNSET)

        retention_till_date: Union[Unset, datetime.datetime] = UNSET
        _retention_till_date = d.pop("retentionTillDate", UNSET)
        if not isinstance(_retention_till_date, Unset):
            retention_till_date = isoparse(_retention_till_date)

        deleted_date: Union[Unset, datetime.datetime] = UNSET
        _deleted_date = d.pop("deletedDate", UNSET)
        if not isinstance(_deleted_date, Unset):
            deleted_date = isoparse(_deleted_date)

        deleted_by: Union[Unset, User] = UNSET
        _deleted_by = d.pop("deletedBy", UNSET)
        if not isinstance(_deleted_by, Unset):
            deleted_by = User.from_dict(_deleted_by)

        archived = d.pop("archived", UNSET)

        archived_date: Union[Unset, datetime.datetime] = UNSET
        _archived_date = d.pop("archivedDate", UNSET)
        if not isinstance(_archived_date, Unset):
            archived_date = isoparse(_archived_date)

        archived_by: Union[Unset, User] = UNSET
        _archived_by = d.pop("archivedBy", UNSET)
        if not isinstance(_archived_by, Unset):
            archived_by = User.from_dict(_archived_by)

        project = cls(
            expand=expand,
            self_=self_,
            id_=id_,
            key=key,
            description=description,
            lead=lead,
            components=components,
            issue_types=issue_types,
            url=url,
            email=email,
            assignee_type=assignee_type,
            versions=versions,
            name=name,
            roles=roles,
            avatar_urls=avatar_urls,
            project_category=project_category,
            project_type_key=project_type_key,
            simplified=simplified,
            style=style,
            favourite=favourite,
            is_private=is_private,
            issue_type_hierarchy=issue_type_hierarchy,
            permissions=permissions,
            properties=properties,
            uuid=uuid,
            insight=insight,
            deleted=deleted,
            retention_till_date=retention_till_date,
            deleted_date=deleted_date,
            deleted_by=deleted_by,
            archived=archived,
            archived_date=archived_date,
            archived_by=archived_by,
        )

        return project
