from dataclasses import dataclass, field
from polzyFunctions.GlobalConstants import GlobalConstants
from datetime import datetime
import json
from logging import getLogger


logger = getLogger(GlobalConstants.loggerName)


class InputFieldTypes:
    """
    These are the input field types, which are used throughout the application. Each inputfieldVisibilityType triggers
    different behavior in the frontend and has different abilities, additional attributes, etc.

    """
    # Just a regular string. May have valueRangeInput, then it is a dropdown. Otherwise only text field.
    # If used with FieldType.output it may have HTML in the value and it will be rendered accordingly.
    TYPESTRING = "Text"

    # A checkbox, which is displayed on the top of the current card or sub-card
    TYPEBOOLEAN = "Flag"
    # A date with date-selector
    TYPEDATETIME = "Datum"
    # A number.
    # May have valueRangeInput=["range", <low>, <high>]
    # If a range is given and inputTriggersComplexupdates = True it will fire a backend-event
    #     after the value was entered.
    # May also be combined with "decimals" and an int of decimal places. Default = 0 decimals = Integers only.
    TYPENUMERIC = "Zahl"
    # A search field for Address endpoint. Seems to be old and replaced by SearchEndPoint
    TYPEADDRESS = "Adresse"
    # A field that will trigger an endpoint and return with a dropdown list. The search field will consume a full line.
    TYPESEARCH = "SearchEndPoint"
    # Long text field
    TYPETEXTBOX = "TextBox"
    # A grid display with Headers and Lineitems
    TYPETABLE = "Table"
    # An Image with interactive (mouseover) capabilities. Don't mix that up with icons or logos, etc.
    TYPEIMAGE = "Image"

    # Like the TYPEBOOLEAN but will consume one full line of the display.
    # You can provide "related_fields" with a list of (slightly differntly) formatted DataFields (as DICT).
    # The problem with those fields is, that they get sent in the activity as regular fields and need to be treated
    # specially in the updateFieldValues-implementation of the corresponding class in order for the sent values
    # to find their way back into the related_fields
    # In the attribute "kurztext" (brief) you may provide valid HTML (e.g. used for longer texts
    TYPEFLAGFULLLINE = "FlagWithOptions"

    # Like the TypeFlagFULLINE but as toggle field with 3 possible values: yes/no/none.
    TYPERADIOWITHOPTIONS = "RadioFlagWithOptions"

    # a Chart-display with various options in value (as DICT)
    # <axis.i.name>: <value> <axis.i.unit>
    # data payload should be a list of lists [x, y]:
    # "values": [
    #        [0, 2115584],
    #        [29, 2263761] ]
    # {
    #         "value": {
    #           "axis": {
    #             "x": {
    #               "name": "Days",
    #               "unit": "d"
    #             },
    #             "y": {
    #               "name": "Amount,
    #               "unit": "$"
    #             }
    #           },
    #           "values": [
    #                [0, 2115584],
    #                [29, 2263761],
    #                ...
    #           ]
    #         }
    #       }
    # Important: Use fieldVisibilityType = FieldVisibilityTypes.output - everything else will not work!
    TYPECHART = "Chart"

    # Specific component used for documents-card of Backend-Antrags
    # fieldVisibilityType may only be 2!
    # value is a list dict objects representing document file {
    # "id": <string: file.id>,
    # "name": <string: filename>,
    # "created": <string: date>,
    # "signed": <string> (for instance: "Yes" or "No"),
    # }
    # See also example in Showcase:
    # lines 175+ of https://gogs.earthsquad.global/athos/PoLZy_Showcase/src/master/antrag.py
    TYPEDOCUMENTS = "Documents"

    # fieldVisibilityType may only be 2!
    # value is a list dict objects representing attached file
    # example in lines 128+ of gogs.earthsquad.global/athos/PoLZy_Showcase/src/master/antrag.py
    # {"id": < string: file.id >,
    # "name": < string: filename >,
    # "created": < string: date >,
    # "type": < string: file.type >,
    # "actions": [ "edit", "delete"] }
    # The supported actions are edit (edit file type) and delete (delete attached document).
    TYPEATTACHMENTS = "Attachments"

    def __init__(self):
        self.types = [
            FieldDataType(typeName=self.TYPESTRING),
            FieldDataType(typeName=self.TYPEBOOLEAN),
            FieldDataType(typeName=self.TYPEDATETIME),
            FieldDataType(typeName=self.TYPENUMERIC),
            FieldDataType(typeName=self.TYPEADDRESS),
            FieldDataType(typeName=self.TYPESEARCH),
            FieldDataType(typeName=self.TYPETEXTBOX),
            FieldDataType(typeName=self.TYPETABLE),
            FieldDataType(typeName=self.TYPEIMAGE),
            FieldDataType(typeName=self.TYPEFLAGFULLLINE),
            FieldDataType(typeName=self.TYPECHART),
            FieldDataType(typeName=self.TYPEDOCUMENTS),
            FieldDataType(typeName=self.TYPEATTACHMENTS),
        ]


@dataclass
class FieldDataType:
    typeName: str

    def toJson(self):
        return self.typeName


@dataclass
class FieldVisibilityTypes:
    """
    Self-explanatory

    """
    # Visible and ready for Input in Frontend
    visible = 1
    # Visible in Frontend. Output only.
    output = 2
    # this field-type will generally not be transferred to the frontend. It will usually not be printed.
    hidden = 3
    # This field-type will not be visible in Frontend but be transferred anyway
    hiddenFrontend = 4


@dataclass
class FieldDefinition:
    name: str = field(default="")
    # This value is a single implementation of usually 2 fields (Value, DefaultValue). When the activity get's executed
    # it's not important whether the user chose the default value or manually selected another value, so 1 field is
    # enough. When the backend wants to set a default value, it writes it in this field for the frontend.
    # Before the frontend can execute the activity, it will write the chosen value from the UI into this field.
    value: any = field(default=None)
    valueTech: any = field(default=None)
    valueOutput: any = field(default=None)
    # The value range is always a list. Either a list with all possible entries or a list with ["range", low, high]
    # for numeric fields. For sliders it is ["slider", low, high].
    valueRangeInput: list = field(default_factory=list)
    # Please check docu in fieldDataType
    fieldDataType: FieldDataType = field(default=FieldDataType)  # Boolean, String, Numeric, etc.
    # for numeric fields only
    decimalPlaces: int = field(default=0)
    # When this flag is set, the frontend will trigger an immediate backend call if the field value changes.
    inputTriggersComplexUpdates: bool = field(default=False)
    shortDescription: str = field(default="")  # Short description, which will be shown in the UI
    tooltip: str = field(default="")  # Tooltip on mouse-over in the UI
    # If this value is set to True, a dropdown list will not allow values other than the ones from ValueRange
    onlyValuesFromValueRange: bool = field(default=False)
    # If True, Frontend will not allow continuation without this field being entered/selected
    isMandatory: bool = field(default=False)
    errorMessage: str = field(default="")  # If a value is set, the frontend will show it as helper to the user.
    fieldVisibilityType: int = field(default=FieldVisibilityTypes.visible)  # See Class FieldVisibilityTypes
    icon: str = field(default="")
    # if the field shall be part of a card = Group, then enter the group-name here. Groups must be defined first
    # using isGroupField=True. The field.name of the group shall go into attribute "group"
    group: str = field(default="")
    # If this is True, then the field is a group-field. Must be boolean.
    # Group-Fields are displayed on the top of the card. They activate/
    # deactivate groups of fields = a card within the card.
    isGroupField: bool = field(default=False)
    # If the value list is too long we can call this endpoint when a value is entered. This is used for instance
    # for address fields to check and provide a value list once the user starts to enter values.
    endpoint: str = field(default="")
    # To group cards further we can create "subtitles" (That are sections within the card). Name here, which subsections
    # you want. Obviously we want to have this attribute only in fields that have also "isGroupField".
    # e.g. ["first section"]
    subtitles: list = field(default_factory=list)
    # If a field shall go into a subsection of the card (see previous attribute) state here the exact name
    # of the section, e.g. "first section" (if you created "first section" within the subtitles of the group.
    subsection: str = field(default="")
    # Option to set colors for the card. Only works with isGroupField=True
    background: str = field(default="")
    # For several FieldDataTypes it is possible to have Child-fields, that will appear only if the host-field has
    # value "true". Here you can pass those additional fields as list.
    relatedFields: list = field(default_factory=list)

    def __post_init__(self):
        pass

    @classmethod
    def stringify(cls, value):
        #
        # stringifies value
        #

        # datetime
        if isinstance(value, datetime):
            return value.strftime("%d-%m-%Y")

        # list or dictionary
        if isinstance(value, (list, dict)):
            return value

        if value is None:
            return value

        # other cases
        return str(value)

    def toJSON(self):
        """
        Generate JSON-String to be sent to Frontend
        :return:
        """

        if hasattr(self, "valueRangeInput") and self.valueRangeInput:
            inputRangeList = [self.stringify(v) for v in self.valueRangeInput]
        else:
            inputRangeList = []

        lValue = self.stringify(self.value)

        # boolean fields with "output" don't work on the frontend. change them to "string" and use valueOutput
        lFieldDataType = self.fieldDataType
        if lFieldDataType == FieldDataType(InputFieldTypes.TYPEBOOLEAN) and self.fieldVisibilityType == FieldVisibilityTypes.output:
            lFieldDataType = FieldDataType(InputFieldTypes.TYPESTRING)
            lValue = self.stringify(self.valueOutput)

        try:
            lReturn = {
                'fieldVisibilityType': self.fieldVisibilityType,
                'name': self.name,
                'brief': self.shortDescription,
                'tooltip': self.tooltip,
                'icon': self.icon,
                'fieldDataType': lFieldDataType.toJson(),
                'inputRange': inputRangeList,
                'onlyFromRange': self.onlyValuesFromValueRange,
                'value': lValue,
                'inputTriggers': self.inputTriggersComplexUpdates,
                'isMandatory': self.isMandatory,
                'errorMessage': self.errorMessage,
                'endpoint': self.endpoint,
                'subtitles': self.subtitles,
                'subsection': self.subsection,
                'backgroundColor': self.background,
                'relatedFields': json.loads(json.dumps(
                    self.relatedFields, default=lambda o: o.toJson() if isinstance(o, FieldDataType) else o)
                ),  # converting FieldDataType object to string, just to avoid errors in json.dumps
            }

            # Remove all empty field values to save space for talking to the frontend
            return {k: v for k, v in lReturn.items() if not self.__checkIfEmptyValue(v)}

        except Exception as e:
            logger.critical(f"Fehler {e}")
            raise ValueError(f"Fehler in toJSON: {e}")

    @staticmethod
    def __checkIfEmptyValue(inValue) -> bool:  # Will return true if empty, flase if not empty.
        if not inValue:
            return True
        if isinstance(inValue, str):
            if len(inValue.strip()) > 0:
                return False
            return True
        if isinstance(inValue, (int, float)):
            return False
        if isinstance(inValue, (list, dict)):
            return len(inValue) == 0
        if isinstance(inValue, FieldVisibilityTypes):
            return False

        logger.info(f"not sure how to handle this field value {inValue}, it's type {type(inValue)}. Will parse to FE")
        return True


class InputFields:
    def __init__(self):
        self.fields: [FieldDefinition] = []

    def addField(self, inputField: FieldDefinition):
        self.fields.append(inputField)

    def getAllInputFields(self) -> [FieldDefinition]:
        return self.fields

    def getAllFieldGroups(self) -> [FieldDefinition]:
        return list(filter(lambda field: field.isGroupField, self.fields))

    def __len__(self):
        return len(self.fields)

    def toJSON(self):
        if not hasattr(self, "fields") or not self.fields:
            return []
        outputList = [f.toJSON() for f in self.fields]
        return outputList

    def getField(self, **kwargs) -> FieldDefinition:
        # returns InputField object matching with given parameters.
        for item in self.fields:
            success = True
            for key, value in kwargs.items():
                try:
                    original_value = getattr(item, key)
                except Exception:
                    original_value = ""
                if original_value != value:
                    success = False
                    break
            if success:
                return item
        return None

    def setField(self, fieldDefinition: FieldDefinition):
        for item in self.fields:
            if item.name == fieldDefinition.name:
                item.fieldVisibilityType = fieldDefinition.fieldVisibilityType
                item.shortDescription = fieldDefinition.shortDescription
                item.isMandatory = fieldDefinition.isMandatory
                item.feldArt = fieldDefinition.fieldDataType
                item.value = fieldDefinition.value
                item.valueTech = fieldDefinition.valueTech
                item.onlyValuesFromValueRange = fieldDefinition.onlyValuesFromValueRange
                item.inputTriggersComplexUpdates = fieldDefinition.inputTriggersComplexUpdates
                item.valueRange = fieldDefinition.valueRangeInput
                item.tooltip = fieldDefinition.tooltip
        # Looks like a new item!
        self.addField(inputField=fieldDefinition)
