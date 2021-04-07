#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@ews-network.net>

"""Definition of Custom::KafkaTopic."""

from copy import deepcopy

from troposphere.cloudformation import AWSCustomObject

from aws_custom_ews_kafka_resources import COMMON_PROPS, TOPIC_COMMON_PROPS, KafkaAclPolicy


class KafkaTopic(AWSCustomObject):
    """
    Class to represent EWS::Kafka::Topic
    """

    resource_type = "Custom::KafkaTopic"

    props = deepcopy(COMMON_PROPS)
    props.update(TOPIC_COMMON_PROPS)
    props.update(
        {
            "ServiceToken": (str, True),
        }
    )


class KafkaAcl(AWSCustomObject):
    """
    Class to represent Custom::KafkaACL
    """

    resource_type = "Custom::KafkaACL"
    props = deepcopy(COMMON_PROPS)
    props.update({"Policies": ([KafkaAclPolicy], True)})
