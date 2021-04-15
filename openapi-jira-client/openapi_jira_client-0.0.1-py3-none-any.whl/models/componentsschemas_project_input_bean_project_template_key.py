from enum import Enum


class ComponentsschemasProjectInputBeanProjectTemplateKey(str, Enum):
    COMPYXISGREENHOPPERJIRAGH_SIMPLIFIED_AGILITY_KANBAN = "com.pyxis.greenhopper.jira:gh-simplified-agility-kanban"
    COMPYXISGREENHOPPERJIRAGH_SIMPLIFIED_AGILITY_SCRUM = "com.pyxis.greenhopper.jira:gh-simplified-agility-scrum"
    COMPYXISGREENHOPPERJIRAGH_SIMPLIFIED_BASIC = "com.pyxis.greenhopper.jira:gh-simplified-basic"
    COMPYXISGREENHOPPERJIRAGH_SIMPLIFIED_KANBAN_CLASSIC = "com.pyxis.greenhopper.jira:gh-simplified-kanban-classic"
    COMPYXISGREENHOPPERJIRAGH_SIMPLIFIED_SCRUM_CLASSIC = "com.pyxis.greenhopper.jira:gh-simplified-scrum-classic"
    COMATLASSIANSERVICEDESKSIMPLIFIED_IT_SERVICE_DESK = "com.atlassian.servicedesk:simplified-it-service-desk"
    COMATLASSIANSERVICEDESKSIMPLIFIED_INTERNAL_SERVICE_DESK = (
        "com.atlassian.servicedesk:simplified-internal-service-desk"
    )
    COMATLASSIANSERVICEDESKSIMPLIFIED_EXTERNAL_SERVICE_DESK = (
        "com.atlassian.servicedesk:simplified-external-service-desk"
    )
    COMATLASSIANSERVICEDESKSIMPLIFIED_HR_SERVICE_DESK = "com.atlassian.servicedesk:simplified-hr-service-desk"
    COMATLASSIANSERVICEDESKSIMPLIFIED_FACILITIES_SERVICE_DESK = (
        "com.atlassian.servicedesk:simplified-facilities-service-desk"
    )
    COMATLASSIANJIRA_CORE_PROJECT_TEMPLATESJIRA_CORE_SIMPLIFIED_CONTENT_MANAGEMENT = (
        "com.atlassian.jira-core-project-templates:jira-core-simplified-content-management"
    )
    COMATLASSIANJIRA_CORE_PROJECT_TEMPLATESJIRA_CORE_SIMPLIFIED_DOCUMENT_APPROVAL = (
        "com.atlassian.jira-core-project-templates:jira-core-simplified-document-approval"
    )
    COMATLASSIANJIRA_CORE_PROJECT_TEMPLATESJIRA_CORE_SIMPLIFIED_LEAD_TRACKING = (
        "com.atlassian.jira-core-project-templates:jira-core-simplified-lead-tracking"
    )
    COMATLASSIANJIRA_CORE_PROJECT_TEMPLATESJIRA_CORE_SIMPLIFIED_PROCESS_CONTROL = (
        "com.atlassian.jira-core-project-templates:jira-core-simplified-process-control"
    )
    COMATLASSIANJIRA_CORE_PROJECT_TEMPLATESJIRA_CORE_SIMPLIFIED_PROCUREMENT = (
        "com.atlassian.jira-core-project-templates:jira-core-simplified-procurement"
    )
    COMATLASSIANJIRA_CORE_PROJECT_TEMPLATESJIRA_CORE_SIMPLIFIED_PROJECT_MANAGEMENT = (
        "com.atlassian.jira-core-project-templates:jira-core-simplified-project-management"
    )
    COMATLASSIANJIRA_CORE_PROJECT_TEMPLATESJIRA_CORE_SIMPLIFIED_RECRUITMENT = (
        "com.atlassian.jira-core-project-templates:jira-core-simplified-recruitment"
    )
    COMATLASSIANJIRA_CORE_PROJECT_TEMPLATESJIRA_CORE_SIMPLIFIED_TASK_ = (
        "com.atlassian.jira-core-project-templates:jira-core-simplified-task-"
    )

    def __str__(self) -> str:
        return str(self.value)
