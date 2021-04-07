# coding: utf-8

"""
    BIMData API

    BIMData API is a tool to interact with your models stored on BIMData’s servers.     Through the API, you can manage your projects, the clouds, upload your IFC files and manage them through endpoints.  # noqa: E501

    The version of the OpenAPI document: v1
    Contact: support@bimdata.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from bimdata_api_client.configuration import Configuration


class IfcExport(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'classifications': 'str',
        'zones': 'str',
        'properties': 'str',
        'systems': 'str',
        'layers': 'str',
        'materials': 'str',
        'attributes': 'str',
        'structure': 'str',
        'uuids': 'list[str]',
        'file_name': 'str'
    }

    attribute_map = {
        'classifications': 'classifications',
        'zones': 'zones',
        'properties': 'properties',
        'systems': 'systems',
        'layers': 'layers',
        'materials': 'materials',
        'attributes': 'attributes',
        'structure': 'structure',
        'uuids': 'uuids',
        'file_name': 'file_name'
    }

    def __init__(self, classifications='UPDATED', zones='UPDATED', properties='UPDATED', systems='UPDATED', layers='UPDATED', materials='UPDATED', attributes='UPDATED', structure='UPDATED', uuids=None, file_name=None, local_vars_configuration=None):  # noqa: E501
        """IfcExport - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._classifications = None
        self._zones = None
        self._properties = None
        self._systems = None
        self._layers = None
        self._materials = None
        self._attributes = None
        self._structure = None
        self._uuids = None
        self._file_name = None
        self.discriminator = None

        if classifications is not None:
            self.classifications = classifications
        if zones is not None:
            self.zones = zones
        if properties is not None:
            self.properties = properties
        if systems is not None:
            self.systems = systems
        if layers is not None:
            self.layers = layers
        if materials is not None:
            self.materials = materials
        if attributes is not None:
            self.attributes = attributes
        if structure is not None:
            self.structure = structure
        if uuids is not None:
            self.uuids = uuids
        self.file_name = file_name

    @property
    def classifications(self):
        """Gets the classifications of this IfcExport.  # noqa: E501

        Exported IFC will include classifications from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include classifications(NONE)  # noqa: E501

        :return: The classifications of this IfcExport.  # noqa: E501
        :rtype: str
        """
        return self._classifications

    @classifications.setter
    def classifications(self, classifications):
        """Sets the classifications of this IfcExport.

        Exported IFC will include classifications from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include classifications(NONE)  # noqa: E501

        :param classifications: The classifications of this IfcExport.  # noqa: E501
        :type: str
        """
        allowed_values = ["ORIGINAL", "UPDATED", "NONE"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and classifications not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `classifications` ({0}), must be one of {1}"  # noqa: E501
                .format(classifications, allowed_values)
            )

        self._classifications = classifications

    @property
    def zones(self):
        """Gets the zones of this IfcExport.  # noqa: E501

        Exported IFC will include zones from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include zones(NONE)  # noqa: E501

        :return: The zones of this IfcExport.  # noqa: E501
        :rtype: str
        """
        return self._zones

    @zones.setter
    def zones(self, zones):
        """Sets the zones of this IfcExport.

        Exported IFC will include zones from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include zones(NONE)  # noqa: E501

        :param zones: The zones of this IfcExport.  # noqa: E501
        :type: str
        """
        allowed_values = ["ORIGINAL", "UPDATED", "NONE"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and zones not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `zones` ({0}), must be one of {1}"  # noqa: E501
                .format(zones, allowed_values)
            )

        self._zones = zones

    @property
    def properties(self):
        """Gets the properties of this IfcExport.  # noqa: E501

        Exported IFC will include properties from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include properties(NONE)  # noqa: E501

        :return: The properties of this IfcExport.  # noqa: E501
        :rtype: str
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this IfcExport.

        Exported IFC will include properties from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include properties(NONE)  # noqa: E501

        :param properties: The properties of this IfcExport.  # noqa: E501
        :type: str
        """
        allowed_values = ["ORIGINAL", "UPDATED", "NONE"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and properties not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `properties` ({0}), must be one of {1}"  # noqa: E501
                .format(properties, allowed_values)
            )

        self._properties = properties

    @property
    def systems(self):
        """Gets the systems of this IfcExport.  # noqa: E501

        Exported IFC will include systems from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include systems(NONE)  # noqa: E501

        :return: The systems of this IfcExport.  # noqa: E501
        :rtype: str
        """
        return self._systems

    @systems.setter
    def systems(self, systems):
        """Sets the systems of this IfcExport.

        Exported IFC will include systems from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include systems(NONE)  # noqa: E501

        :param systems: The systems of this IfcExport.  # noqa: E501
        :type: str
        """
        allowed_values = ["ORIGINAL", "UPDATED", "NONE"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and systems not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `systems` ({0}), must be one of {1}"  # noqa: E501
                .format(systems, allowed_values)
            )

        self._systems = systems

    @property
    def layers(self):
        """Gets the layers of this IfcExport.  # noqa: E501

        Exported IFC will include layers from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include layers(NONE)  # noqa: E501

        :return: The layers of this IfcExport.  # noqa: E501
        :rtype: str
        """
        return self._layers

    @layers.setter
    def layers(self, layers):
        """Sets the layers of this IfcExport.

        Exported IFC will include layers from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include layers(NONE)  # noqa: E501

        :param layers: The layers of this IfcExport.  # noqa: E501
        :type: str
        """
        allowed_values = ["ORIGINAL", "UPDATED", "NONE"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and layers not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `layers` ({0}), must be one of {1}"  # noqa: E501
                .format(layers, allowed_values)
            )

        self._layers = layers

    @property
    def materials(self):
        """Gets the materials of this IfcExport.  # noqa: E501

        Exported IFC will include materials from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include materials(NONE)  # noqa: E501

        :return: The materials of this IfcExport.  # noqa: E501
        :rtype: str
        """
        return self._materials

    @materials.setter
    def materials(self, materials):
        """Sets the materials of this IfcExport.

        Exported IFC will include materials from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include materials(NONE)  # noqa: E501

        :param materials: The materials of this IfcExport.  # noqa: E501
        :type: str
        """
        allowed_values = ["ORIGINAL", "UPDATED", "NONE"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and materials not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `materials` ({0}), must be one of {1}"  # noqa: E501
                .format(materials, allowed_values)
            )

        self._materials = materials

    @property
    def attributes(self):
        """Gets the attributes of this IfcExport.  # noqa: E501

        Exported IFC will include attributes from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include attributes(NONE)  # noqa: E501

        :return: The attributes of this IfcExport.  # noqa: E501
        :rtype: str
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """Sets the attributes of this IfcExport.

        Exported IFC will include attributes from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include attributes(NONE)  # noqa: E501

        :param attributes: The attributes of this IfcExport.  # noqa: E501
        :type: str
        """
        allowed_values = ["ORIGINAL", "UPDATED", "NONE"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and attributes not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `attributes` ({0}), must be one of {1}"  # noqa: E501
                .format(attributes, allowed_values)
            )

        self._attributes = attributes

    @property
    def structure(self):
        """Gets the structure of this IfcExport.  # noqa: E501

        Exported IFC will include the structure from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include structure(NONE)  # noqa: E501

        :return: The structure of this IfcExport.  # noqa: E501
        :rtype: str
        """
        return self._structure

    @structure.setter
    def structure(self, structure):
        """Sets the structure of this IfcExport.

        Exported IFC will include the structure from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won't include structure(NONE)  # noqa: E501

        :param structure: The structure of this IfcExport.  # noqa: E501
        :type: str
        """
        allowed_values = ["ORIGINAL", "UPDATED", "NONE"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and structure not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `structure` ({0}), must be one of {1}"  # noqa: E501
                .format(structure, allowed_values)
            )

        self._structure = structure

    @property
    def uuids(self):
        """Gets the uuids of this IfcExport.  # noqa: E501

          # noqa: E501

        :return: The uuids of this IfcExport.  # noqa: E501
        :rtype: list[str]
        """
        return self._uuids

    @uuids.setter
    def uuids(self, uuids):
        """Sets the uuids of this IfcExport.

          # noqa: E501

        :param uuids: The uuids of this IfcExport.  # noqa: E501
        :type: list[str]
        """

        self._uuids = uuids

    @property
    def file_name(self):
        """Gets the file_name of this IfcExport.  # noqa: E501

        The name of the exported IFC file. It MUST end with .ifc or the exported file won't be processed by BIMData  # noqa: E501

        :return: The file_name of this IfcExport.  # noqa: E501
        :rtype: str
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        """Sets the file_name of this IfcExport.

        The name of the exported IFC file. It MUST end with .ifc or the exported file won't be processed by BIMData  # noqa: E501

        :param file_name: The file_name of this IfcExport.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and file_name is None:  # noqa: E501
            raise ValueError("Invalid value for `file_name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                file_name is not None and len(file_name) > 512):
            raise ValueError("Invalid value for `file_name`, length must be less than or equal to `512`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                file_name is not None and len(file_name) < 1):
            raise ValueError("Invalid value for `file_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._file_name = file_name

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, IfcExport):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, IfcExport):
            return True

        return self.to_dict() != other.to_dict()
