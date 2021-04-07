#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@ews-network.net>

"""Definition of EWS::Kafka::Topic resource."""

from copy import deepcopy
from troposphere import AWSObject

from aws_custom_ews_kafka_resources import COMMON_PROPS, TOPIC_COMMON_PROPS, KafkaAclPolicy


class KafkaTopic(AWSObject):
    """
    Class to represent EWS::Kafka::Topic
    """

    resource_type = "EWS::Kafka::Topic"
    props = deepcopy(COMMON_PROPS)
    props.update(TOPIC_COMMON_PROPS)


class KafkaAcl(AWSObject):
    """
    Class to represent EWS::Kafka::ACL
    """

    resource_type = "EWS::Kafka::ACL"
    props = deepcopy(COMMON_PROPS)
    props.update({"Policies": ([KafkaAclPolicy], True)})
