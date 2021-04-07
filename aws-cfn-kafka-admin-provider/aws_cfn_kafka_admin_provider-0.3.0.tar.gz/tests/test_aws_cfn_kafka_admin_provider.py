#!/usr/bin/env python

"""Tests for `aws_cfn_kafka_admin_provider` package."""

from os import path
import pytest


from aws_cfn_kafka_admin_provider.aws_cfn_kafka_admin_provider import KafkaStack


def test_valid_custom_resource_input():
    """
    Function to test valid input
    :return:
    """
    here = path.abspath(path.dirname(__file__))
    c = KafkaStack(f"{here}/valid_input_custom.yaml")
    c.render_topics()
    print(c.template.to_yaml())


def test_valid_private_resource_input():
    """
    Function to test valid input
    :return:
    """
    here = path.abspath(path.dirname(__file__))
    c = KafkaStack(f"{here}/valid_input_resource.yaml")
    c.render_topics()
    print(c.template.to_yaml())


def test_invalid_custom_resource_input():
    """
    Function to test valid input
    :return:
    """
    here = path.abspath(path.dirname(__file__))
    with pytest.raises(ValueError):
        c = KafkaStack(f"{here}/invalid_input_custom.yaml")
        c.render_topics()
        c.template.to_yaml()


def test_invalid_private_resource_input():
    """
    Function to test valid input
    :return:
    """
    here = path.abspath(path.dirname(__file__))
    with pytest.raises(ValueError):
        c = KafkaStack(f"{here}/invalid_input_resource.yaml")
        c.render_topics()
        c.template.to_yaml()
