from enum import Enum


class SearchProjectsOrderBy(str, Enum):
    CATEGORY = "category"
    VALUE_1 = "-category"
    VALUE_2 = "+category"
    KEY = "key"
    VALUE_4 = "-key"
    VALUE_5 = "+key"
    NAME = "name"
    VALUE_7 = "-name"
    VALUE_8 = "+name"
    OWNER = "owner"
    VALUE_10 = "-owner"
    VALUE_11 = "+owner"
    ISSUECOUNT = "issueCount"
    VALUE_13 = "-issueCount"
    VALUE_14 = "+issueCount"
    LASTISSUEUPDATEDDATE = "lastIssueUpdatedDate"
    VALUE_16 = "-lastIssueUpdatedDate"
    VALUE_17 = "+lastIssueUpdatedDate"
    ARCHIVEDDATE = "archivedDate"
    VALUE_19 = "+archivedDate"
    VALUE_20 = "-archivedDate"
    DELETEDDATE = "deletedDate"
    VALUE_22 = "+deletedDate"
    VALUE_23 = "-deletedDate"

    def __str__(self) -> str:
        return str(self.value)
