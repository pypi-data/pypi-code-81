from enum import Enum


class ComponentsschemasWebhookDetailsEventsItem(str, Enum):
    JIRAISSUE_CREATED = "jira:issue_created"
    JIRAISSUE_UPDATED = "jira:issue_updated"
    JIRAISSUE_DELETED = "jira:issue_deleted"
    COMMENT_CREATED = "comment_created"
    COMMENT_UPDATED = "comment_updated"
    COMMENT_DELETED = "comment_deleted"
    ISSUE_PROPERTY_SET = "issue_property_set"
    ISSUE_PROPERTY_DELETED = "issue_property_deleted"

    def __str__(self) -> str:
        return str(self.value)
