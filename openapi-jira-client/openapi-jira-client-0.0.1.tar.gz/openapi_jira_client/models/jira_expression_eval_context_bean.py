from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.id_or_key_bean import IdOrKeyBean
from ..models.jexp_issues import JexpIssues
from ..types import UNSET, Unset

T = TypeVar("T", bound="JiraExpressionEvalContextBean")


@attr.s(auto_attribs=True)
class JiraExpressionEvalContextBean:
    """  """

    issue: Union[Unset, IdOrKeyBean] = UNSET
    issues: Union[Unset, JexpIssues] = UNSET
    project: Union[Unset, IdOrKeyBean] = UNSET
    sprint: Union[Unset, int] = UNSET
    board: Union[Unset, int] = UNSET
    service_desk: Union[Unset, int] = UNSET
    customer_request: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        issue: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.issue, Unset):
            issue = self.issue.to_dict()

        issues: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.issues, Unset):
            issues = self.issues.to_dict()

        project: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.project, Unset):
            project = self.project.to_dict()

        sprint = self.sprint
        board = self.board
        service_desk = self.service_desk
        customer_request = self.customer_request

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if issue is not UNSET:
            field_dict["issue"] = issue
        if issues is not UNSET:
            field_dict["issues"] = issues
        if project is not UNSET:
            field_dict["project"] = project
        if sprint is not UNSET:
            field_dict["sprint"] = sprint
        if board is not UNSET:
            field_dict["board"] = board
        if service_desk is not UNSET:
            field_dict["serviceDesk"] = service_desk
        if customer_request is not UNSET:
            field_dict["customerRequest"] = customer_request

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue: Union[Unset, IdOrKeyBean] = UNSET
        _issue = d.pop("issue", UNSET)
        if not isinstance(_issue, Unset):
            issue = IdOrKeyBean.from_dict(_issue)

        issues: Union[Unset, JexpIssues] = UNSET
        _issues = d.pop("issues", UNSET)
        if not isinstance(_issues, Unset):
            issues = JexpIssues.from_dict(_issues)

        project: Union[Unset, IdOrKeyBean] = UNSET
        _project = d.pop("project", UNSET)
        if not isinstance(_project, Unset):
            project = IdOrKeyBean.from_dict(_project)

        sprint = d.pop("sprint", UNSET)

        board = d.pop("board", UNSET)

        service_desk = d.pop("serviceDesk", UNSET)

        customer_request = d.pop("customerRequest", UNSET)

        jira_expression_eval_context_bean = cls(
            issue=issue,
            issues=issues,
            project=project,
            sprint=sprint,
            board=board,
            service_desk=service_desk,
            customer_request=customer_request,
        )

        return jira_expression_eval_context_bean
