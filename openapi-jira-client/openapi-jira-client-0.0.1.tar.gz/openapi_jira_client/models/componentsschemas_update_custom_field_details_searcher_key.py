from enum import Enum


class ComponentsschemasUpdateCustomFieldDetailsSearcherKey(str, Enum):
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESCASCADINGSELECTSEARCHER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:cascadingselectsearcher"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESDATERANGE = (
        "com.atlassian.jira.plugin.system.customfieldtypes:daterange"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESDATETIMERANGE = (
        "com.atlassian.jira.plugin.system.customfieldtypes:datetimerange"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESEXACTNUMBER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:exactnumber"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESEXACTTEXTSEARCHER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:exacttextsearcher"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESGROUPPICKERSEARCHER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:grouppickersearcher"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESLABELSEARCHER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:labelsearcher"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESMULTISELECTSEARCHER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESNUMBERRANGE = (
        "com.atlassian.jira.plugin.system.customfieldtypes:numberrange"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESPROJECTSEARCHER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:projectsearcher"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESTEXTSEARCHER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:textsearcher"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESUSERPICKERGROUPSEARCHER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:userpickergroupsearcher"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESVERSIONSEARCHER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:versionsearcher"
    )

    def __str__(self) -> str:
        return str(self.value)
