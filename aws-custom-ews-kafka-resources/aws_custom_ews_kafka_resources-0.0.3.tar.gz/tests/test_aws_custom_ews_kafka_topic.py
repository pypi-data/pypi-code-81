#!/usr/bin/env python

"""Tests for `aws_custom_ews_kafka_resources` package."""

from pytest import raises
from troposphere import Template

from aws_custom_ews_kafka_resources.resource import KafkaTopic as Resource
from aws_custom_ews_kafka_resources.custom import KafkaTopic as Custom


def test_kafka_rtopics():
    """
    Function to test normal working of the
    :return:
    """
    template = Template()
    r_topic = Resource(
        "newtopic",
        Name="my-new-topic",
        PartitionsCount=6,
        BootstrapServers="broker.cluster.internal",
    )
    template.add_resource(r_topic)
    template.to_json()


def test_kafka_ctopics():
    template = Template()
    c_topic = Custom(
        "newtopiccustom",
        ServiceToken="arn:aws:lambda:eu-west-1:012345678912:function:name",
        Name="my-new-topic",
        PartitionsCount=6,
        BootstrapServers="broker.cluster.internal",
        Settings={
            "flush.retry": "5"
        }
    )
    template.add_resource(c_topic)
    template.to_json()


def test_negative_kafka_rtopics():
    """
    Function to test normal working of the
    :return:
    """
    with raises(ValueError):
        Resource(
            "newtopic",
            Name="my-new-topic",
            PartitionsCount=-1,
            BootstrapServers="broker.cluster.internal",
        )


def test_negative_kafka_ctopics():
    """
    Function to negative test custom topic
    :return:
    """
    with raises(ValueError):
        Custom(
            "newtopic",
            ServiceToken="arn:aws:lambda:eu-west-1:012345678912:function:name",
            Name="my-new-topic",
            PartitionsCount=-2,
            BootstrapServers="broker.cluster.internal",
        )
