# coding: utf-8

"""
    Cognite API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: playground
    Contact: support@cognite.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from cognite.geospatial._client.configuration import Configuration


class GeometrySpatialFilterDTO(object):
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
        'spatial_relationship': 'SpatialRelationshipDTO',
        'geometry': 'GeometryDTO'
    }

    attribute_map = {
        'spatial_relationship': 'spatialRelationship',
        'geometry': 'geometry'
    }

    def __init__(self, spatial_relationship=None, geometry=None, local_vars_configuration=None):  # noqa: E501
        """GeometrySpatialFilterDTO - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._spatial_relationship = None
        self._geometry = None
        self.discriminator = None

        self.spatial_relationship = spatial_relationship
        self.geometry = geometry

    @property
    def spatial_relationship(self):
        """Gets the spatial_relationship of this GeometrySpatialFilterDTO.  # noqa: E501


        :return: The spatial_relationship of this GeometrySpatialFilterDTO.  # noqa: E501
        :rtype: SpatialRelationshipDTO
        """
        return self._spatial_relationship

    @spatial_relationship.setter
    def spatial_relationship(self, spatial_relationship):
        """Sets the spatial_relationship of this GeometrySpatialFilterDTO.


        :param spatial_relationship: The spatial_relationship of this GeometrySpatialFilterDTO.  # noqa: E501
        :type spatial_relationship: SpatialRelationshipDTO
        """
        if self.local_vars_configuration.client_side_validation and spatial_relationship is None:  # noqa: E501
            raise ValueError("Invalid value for `spatial_relationship`, must not be `None`")  # noqa: E501

        self._spatial_relationship = spatial_relationship

    @property
    def geometry(self):
        """Gets the geometry of this GeometrySpatialFilterDTO.  # noqa: E501


        :return: The geometry of this GeometrySpatialFilterDTO.  # noqa: E501
        :rtype: GeometryDTO
        """
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Sets the geometry of this GeometrySpatialFilterDTO.


        :param geometry: The geometry of this GeometrySpatialFilterDTO.  # noqa: E501
        :type geometry: GeometryDTO
        """
        if self.local_vars_configuration.client_side_validation and geometry is None:  # noqa: E501
            raise ValueError("Invalid value for `geometry`, must not be `None`")  # noqa: E501

        self._geometry = geometry

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
        if not isinstance(other, GeometrySpatialFilterDTO):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GeometrySpatialFilterDTO):
            return True

        return self.to_dict() != other.to_dict()
