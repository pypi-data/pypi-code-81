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


class FullTopic(object):
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
        'guid': 'str',
        'creation_date': 'datetime',
        'creation_author': 'str',
        'modified_date': 'datetime',
        'modified_author': 'str',
        'title': 'str',
        'description': 'str',
        'reference_links': 'list[str]',
        'ifcs': 'list[int]',
        'labels': 'list[str]',
        'topic_type': 'str',
        'topic_status': 'str',
        'stage': 'str',
        'priority': 'str',
        'index': 'int',
        'assigned_to': 'str',
        'format': 'str',
        'due_date': 'datetime',
        'comments': 'list[Comment]',
        'viewpoints': 'list[Viewpoint]',
        'project': 'int'
    }

    attribute_map = {
        'guid': 'guid',
        'creation_date': 'creation_date',
        'creation_author': 'creation_author',
        'modified_date': 'modified_date',
        'modified_author': 'modified_author',
        'title': 'title',
        'description': 'description',
        'reference_links': 'reference_links',
        'ifcs': 'ifcs',
        'labels': 'labels',
        'topic_type': 'topic_type',
        'topic_status': 'topic_status',
        'stage': 'stage',
        'priority': 'priority',
        'index': 'index',
        'assigned_to': 'assigned_to',
        'format': 'format',
        'due_date': 'due_date',
        'comments': 'comments',
        'viewpoints': 'viewpoints',
        'project': 'project'
    }

    def __init__(self, guid=None, creation_date=None, creation_author=None, modified_date=None, modified_author=None, title=None, description=None, reference_links=None, ifcs=None, labels=None, topic_type=None, topic_status=None, stage=None, priority=None, index=None, assigned_to=None, format=None, due_date=None, comments=None, viewpoints=None, project=None, local_vars_configuration=None):  # noqa: E501
        """FullTopic - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._guid = None
        self._creation_date = None
        self._creation_author = None
        self._modified_date = None
        self._modified_author = None
        self._title = None
        self._description = None
        self._reference_links = None
        self._ifcs = None
        self._labels = None
        self._topic_type = None
        self._topic_status = None
        self._stage = None
        self._priority = None
        self._index = None
        self._assigned_to = None
        self._format = None
        self._due_date = None
        self._comments = None
        self._viewpoints = None
        self._project = None
        self.discriminator = None

        if guid is not None:
            self.guid = guid
        if creation_date is not None:
            self.creation_date = creation_date
        self.creation_author = creation_author
        if modified_date is not None:
            self.modified_date = modified_date
        self.modified_author = modified_author
        self.title = title
        self.description = description
        self.reference_links = reference_links
        if ifcs is not None:
            self.ifcs = ifcs
        self.labels = labels
        self.topic_type = topic_type
        self.topic_status = topic_status
        self.stage = stage
        self.priority = priority
        self.index = index
        self.assigned_to = assigned_to
        if format is not None:
            self.format = format
        self.due_date = due_date
        if comments is not None:
            self.comments = comments
        if viewpoints is not None:
            self.viewpoints = viewpoints
        self.project = project

    @property
    def guid(self):
        """Gets the guid of this FullTopic.  # noqa: E501


        :return: The guid of this FullTopic.  # noqa: E501
        :rtype: str
        """
        return self._guid

    @guid.setter
    def guid(self, guid):
        """Sets the guid of this FullTopic.


        :param guid: The guid of this FullTopic.  # noqa: E501
        :type: str
        """

        self._guid = guid

    @property
    def creation_date(self):
        """Gets the creation_date of this FullTopic.  # noqa: E501


        :return: The creation_date of this FullTopic.  # noqa: E501
        :rtype: datetime
        """
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        """Sets the creation_date of this FullTopic.


        :param creation_date: The creation_date of this FullTopic.  # noqa: E501
        :type: datetime
        """

        self._creation_date = creation_date

    @property
    def creation_author(self):
        """Gets the creation_author of this FullTopic.  # noqa: E501


        :return: The creation_author of this FullTopic.  # noqa: E501
        :rtype: str
        """
        return self._creation_author

    @creation_author.setter
    def creation_author(self, creation_author):
        """Sets the creation_author of this FullTopic.


        :param creation_author: The creation_author of this FullTopic.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                creation_author is not None and len(creation_author) > 254):
            raise ValueError("Invalid value for `creation_author`, length must be less than or equal to `254`")  # noqa: E501

        self._creation_author = creation_author

    @property
    def modified_date(self):
        """Gets the modified_date of this FullTopic.  # noqa: E501


        :return: The modified_date of this FullTopic.  # noqa: E501
        :rtype: datetime
        """
        return self._modified_date

    @modified_date.setter
    def modified_date(self, modified_date):
        """Sets the modified_date of this FullTopic.


        :param modified_date: The modified_date of this FullTopic.  # noqa: E501
        :type: datetime
        """

        self._modified_date = modified_date

    @property
    def modified_author(self):
        """Gets the modified_author of this FullTopic.  # noqa: E501


        :return: The modified_author of this FullTopic.  # noqa: E501
        :rtype: str
        """
        return self._modified_author

    @modified_author.setter
    def modified_author(self, modified_author):
        """Sets the modified_author of this FullTopic.


        :param modified_author: The modified_author of this FullTopic.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                modified_author is not None and len(modified_author) > 254):
            raise ValueError("Invalid value for `modified_author`, length must be less than or equal to `254`")  # noqa: E501

        self._modified_author = modified_author

    @property
    def title(self):
        """Gets the title of this FullTopic.  # noqa: E501


        :return: The title of this FullTopic.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this FullTopic.


        :param title: The title of this FullTopic.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and title is None:  # noqa: E501
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                title is not None and len(title) < 1):
            raise ValueError("Invalid value for `title`, length must be greater than or equal to `1`")  # noqa: E501

        self._title = title

    @property
    def description(self):
        """Gets the description of this FullTopic.  # noqa: E501


        :return: The description of this FullTopic.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this FullTopic.


        :param description: The description of this FullTopic.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def reference_links(self):
        """Gets the reference_links of this FullTopic.  # noqa: E501

          # noqa: E501

        :return: The reference_links of this FullTopic.  # noqa: E501
        :rtype: list[str]
        """
        return self._reference_links

    @reference_links.setter
    def reference_links(self, reference_links):
        """Sets the reference_links of this FullTopic.

          # noqa: E501

        :param reference_links: The reference_links of this FullTopic.  # noqa: E501
        :type: list[str]
        """

        self._reference_links = reference_links

    @property
    def ifcs(self):
        """Gets the ifcs of this FullTopic.  # noqa: E501


        :return: The ifcs of this FullTopic.  # noqa: E501
        :rtype: list[int]
        """
        return self._ifcs

    @ifcs.setter
    def ifcs(self, ifcs):
        """Sets the ifcs of this FullTopic.


        :param ifcs: The ifcs of this FullTopic.  # noqa: E501
        :type: list[int]
        """

        self._ifcs = ifcs

    @property
    def labels(self):
        """Gets the labels of this FullTopic.  # noqa: E501

          # noqa: E501

        :return: The labels of this FullTopic.  # noqa: E501
        :rtype: list[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this FullTopic.

          # noqa: E501

        :param labels: The labels of this FullTopic.  # noqa: E501
        :type: list[str]
        """

        self._labels = labels

    @property
    def topic_type(self):
        """Gets the topic_type of this FullTopic.  # noqa: E501


        :return: The topic_type of this FullTopic.  # noqa: E501
        :rtype: str
        """
        return self._topic_type

    @topic_type.setter
    def topic_type(self, topic_type):
        """Sets the topic_type of this FullTopic.


        :param topic_type: The topic_type of this FullTopic.  # noqa: E501
        :type: str
        """

        self._topic_type = topic_type

    @property
    def topic_status(self):
        """Gets the topic_status of this FullTopic.  # noqa: E501


        :return: The topic_status of this FullTopic.  # noqa: E501
        :rtype: str
        """
        return self._topic_status

    @topic_status.setter
    def topic_status(self, topic_status):
        """Sets the topic_status of this FullTopic.


        :param topic_status: The topic_status of this FullTopic.  # noqa: E501
        :type: str
        """

        self._topic_status = topic_status

    @property
    def stage(self):
        """Gets the stage of this FullTopic.  # noqa: E501


        :return: The stage of this FullTopic.  # noqa: E501
        :rtype: str
        """
        return self._stage

    @stage.setter
    def stage(self, stage):
        """Sets the stage of this FullTopic.


        :param stage: The stage of this FullTopic.  # noqa: E501
        :type: str
        """

        self._stage = stage

    @property
    def priority(self):
        """Gets the priority of this FullTopic.  # noqa: E501


        :return: The priority of this FullTopic.  # noqa: E501
        :rtype: str
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this FullTopic.


        :param priority: The priority of this FullTopic.  # noqa: E501
        :type: str
        """

        self._priority = priority

    @property
    def index(self):
        """Gets the index of this FullTopic.  # noqa: E501


        :return: The index of this FullTopic.  # noqa: E501
        :rtype: int
        """
        return self._index

    @index.setter
    def index(self, index):
        """Sets the index of this FullTopic.


        :param index: The index of this FullTopic.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                index is not None and index > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `index`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                index is not None and index < 0):  # noqa: E501
            raise ValueError("Invalid value for `index`, must be a value greater than or equal to `0`")  # noqa: E501

        self._index = index

    @property
    def assigned_to(self):
        """Gets the assigned_to of this FullTopic.  # noqa: E501


        :return: The assigned_to of this FullTopic.  # noqa: E501
        :rtype: str
        """
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, assigned_to):
        """Sets the assigned_to of this FullTopic.


        :param assigned_to: The assigned_to of this FullTopic.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                assigned_to is not None and len(assigned_to) > 254):
            raise ValueError("Invalid value for `assigned_to`, length must be less than or equal to `254`")  # noqa: E501

        self._assigned_to = assigned_to

    @property
    def format(self):
        """Gets the format of this FullTopic.  # noqa: E501


        :return: The format of this FullTopic.  # noqa: E501
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """Sets the format of this FullTopic.


        :param format: The format of this FullTopic.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                format is not None and len(format) > 64):
            raise ValueError("Invalid value for `format`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                format is not None and len(format) < 1):
            raise ValueError("Invalid value for `format`, length must be greater than or equal to `1`")  # noqa: E501

        self._format = format

    @property
    def due_date(self):
        """Gets the due_date of this FullTopic.  # noqa: E501


        :return: The due_date of this FullTopic.  # noqa: E501
        :rtype: datetime
        """
        return self._due_date

    @due_date.setter
    def due_date(self, due_date):
        """Sets the due_date of this FullTopic.


        :param due_date: The due_date of this FullTopic.  # noqa: E501
        :type: datetime
        """

        self._due_date = due_date

    @property
    def comments(self):
        """Gets the comments of this FullTopic.  # noqa: E501

          # noqa: E501

        :return: The comments of this FullTopic.  # noqa: E501
        :rtype: list[Comment]
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """Sets the comments of this FullTopic.

          # noqa: E501

        :param comments: The comments of this FullTopic.  # noqa: E501
        :type: list[Comment]
        """

        self._comments = comments

    @property
    def viewpoints(self):
        """Gets the viewpoints of this FullTopic.  # noqa: E501

          # noqa: E501

        :return: The viewpoints of this FullTopic.  # noqa: E501
        :rtype: list[Viewpoint]
        """
        return self._viewpoints

    @viewpoints.setter
    def viewpoints(self, viewpoints):
        """Sets the viewpoints of this FullTopic.

          # noqa: E501

        :param viewpoints: The viewpoints of this FullTopic.  # noqa: E501
        :type: list[Viewpoint]
        """

        self._viewpoints = viewpoints

    @property
    def project(self):
        """Gets the project of this FullTopic.  # noqa: E501


        :return: The project of this FullTopic.  # noqa: E501
        :rtype: int
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this FullTopic.


        :param project: The project of this FullTopic.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and project is None:  # noqa: E501
            raise ValueError("Invalid value for `project`, must not be `None`")  # noqa: E501

        self._project = project

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
        if not isinstance(other, FullTopic):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FullTopic):
            return True

        return self.to_dict() != other.to_dict()
