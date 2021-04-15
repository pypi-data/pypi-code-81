from enum import Enum


class ComponentsschemasCustomFieldDefinitionJsonBeanType(str, Enum):
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESCASCADINGSELECT = (
        "com.atlassian.jira.plugin.system.customfieldtypes:cascadingselect"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESDATEPICKER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:datepicker"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESDATETIME = "com.atlassian.jira.plugin.system.customfieldtypes:datetime"
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESFLOAT = "com.atlassian.jira.plugin.system.customfieldtypes:float"
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESGROUPPICKER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:grouppicker"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESIMPORTID = "com.atlassian.jira.plugin.system.customfieldtypes:importid"
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESLABELS = "com.atlassian.jira.plugin.system.customfieldtypes:labels"
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESMULTICHECKBOXES = (
        "com.atlassian.jira.plugin.system.customfieldtypes:multicheckboxes"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESMULTIGROUPPICKER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:multigrouppicker"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESMULTISELECT = (
        "com.atlassian.jira.plugin.system.customfieldtypes:multiselect"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESMULTIUSERPICKER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:multiuserpicker"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESMULTIVERSION = (
        "com.atlassian.jira.plugin.system.customfieldtypes:multiversion"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESPROJECT = "com.atlassian.jira.plugin.system.customfieldtypes:project"
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESRADIOBUTTONS = (
        "com.atlassian.jira.plugin.system.customfieldtypes:radiobuttons"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESREADONLYFIELD = (
        "com.atlassian.jira.plugin.system.customfieldtypes:readonlyfield"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESSELECT = "com.atlassian.jira.plugin.system.customfieldtypes:select"
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESTEXTAREA = "com.atlassian.jira.plugin.system.customfieldtypes:textarea"
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESTEXTFIELD = (
        "com.atlassian.jira.plugin.system.customfieldtypes:textfield"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESURL = "com.atlassian.jira.plugin.system.customfieldtypes:url"
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESUSERPICKER = (
        "com.atlassian.jira.plugin.system.customfieldtypes:userpicker"
    )
    COMATLASSIANJIRAPLUGINSYSTEMCUSTOMFIELDTYPESVERSION = "com.atlassian.jira.plugin.system.customfieldtypes:version"

    def __str__(self) -> str:
        return str(self.value)
