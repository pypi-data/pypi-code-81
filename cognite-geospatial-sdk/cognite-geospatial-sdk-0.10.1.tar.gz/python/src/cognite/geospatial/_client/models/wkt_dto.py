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


class WktDTO(object):
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
        'wkt': 'str',
        'crs': 'str'
    }

    attribute_map = {
        'wkt': 'wkt',
        'crs': 'crs'
    }

    def __init__(self, wkt=None, crs=None, local_vars_configuration=None):  # noqa: E501
        """WktDTO - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._wkt = None
        self._crs = None
        self.discriminator = None

        self.wkt = wkt
        self.crs = crs

    @property
    def wkt(self):
        """Gets the wkt of this WktDTO.  # noqa: E501


        :return: The wkt of this WktDTO.  # noqa: E501
        :rtype: str
        """
        return self._wkt

    @wkt.setter
    def wkt(self, wkt):
        """Sets the wkt of this WktDTO.


        :param wkt: The wkt of this WktDTO.  # noqa: E501
        :type wkt: str
        """
        if self.local_vars_configuration.client_side_validation and wkt is None:  # noqa: E501
            raise ValueError("Invalid value for `wkt`, must not be `None`")  # noqa: E501

        self._wkt = wkt

    @property
    def crs(self):
        """Gets the crs of this WktDTO.  # noqa: E501


        :return: The crs of this WktDTO.  # noqa: E501
        :rtype: str
        """
        return self._crs

    @crs.setter
    def crs(self, crs):
        """Sets the crs of this WktDTO.


        :param crs: The crs of this WktDTO.  # noqa: E501
        :type crs: str
        """
        if self.local_vars_configuration.client_side_validation and crs is None:  # noqa: E501
            raise ValueError("Invalid value for `crs`, must not be `None`")  # noqa: E501

        self._crs = crs

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
        if not isinstance(other, WktDTO):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, WktDTO):
            return True

        return self.to_dict() != other.to_dict()
