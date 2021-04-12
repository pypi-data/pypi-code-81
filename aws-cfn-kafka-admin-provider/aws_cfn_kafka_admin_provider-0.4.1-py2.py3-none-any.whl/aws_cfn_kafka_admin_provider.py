#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@ews-network.net>


"""Main module."""

import re
from copy import deepcopy

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from troposphere import Template
from troposphere import Ref, Sub, GetAtt
from troposphere import AWS_NO_VALUE
from cfn_tools import CfnYamlLoader

from aws_custom_ews_kafka_resources import KafkaAclPolicy
from aws_custom_ews_kafka_resources.custom import (
    KafkaTopic as CTopic,
    KafkaAcl as CACLs,
)
from aws_custom_ews_kafka_resources.resource import (
    KafkaTopic as RTopic,
    KafkaAcl as RACLs,
)

from .model import (
    Model,
    EwsKafkaParmeters,
    Topics,
    ACLs,
    SecurityProtocol,
    SASLMechanism,
)
from .model import Policy, Action, ResourceType, PatternType, Effect

NONALPHANUM = re.compile(r"([^a-zA-Z0-9]+)")


def keyisset(x, y):
    """
    Macro to figure if the the dictionary contains a key and that the key is not empty

    :param x: The key to check presence in the dictionary
    :type x: str
    :param y: The dictionary to check for
    :type y: dict

    :returns: True/False
    :rtype: bool
    """
    if isinstance(y, dict) and x in y.keys() and y[x]:
        return True
    return False


def keypresent(x, y):
    """
    Macro to figure if the the dictionary contains a key and that the key is not empty

    :param x: The key to check presence in the dictionary
    :type x: str
    :param y: The dictionary to check for
    :type y: dict

    :returns: True/False
    :rtype: bool
    """
    if isinstance(y, dict) and x in y.keys():
        return True
    return False


def merge_topics(final, override, extend_all=False):
    """
    Function to override and update settings from override to primary
    Topics are filtered out via the Name property

    :param dict final:
    :param dict override:
    :param extend_all: Whether the policies or ACLs can be merged.
    :return: The final merged dict
    :rtype: dict
    """
    if keyisset("Topics", override):
        override_topics = Topics.parse_obj(override["Topics"]).dict()
        if not extend_all and not keypresent("Topics", override_topics):
            del override_topics["Topics"]
            final["Topics"].update(override_topics)
        elif (
            extend_all
            and keyisset("Topics", override_topics)
            and keyisset("Topics", final["Topics"])
        ):
            merged_lists = override_topics["Topics"] + final["Topics"]["Topics"]
            topics = list({v["Name"]: v for v in merged_lists}.values())
            final["Topics"].update(override_topics)
            final["Topics"]["Topics"] = topics


def merge_acls(final, override, extend_all=False):
    """
    Function to override and update settings from override to primary
    All ACL policy is a dictionary made of simple objects, no key filtering

    :param dict final:
    :param dict override:
    :param extend_all: Whether the policies or ACLs can be merged.
    :return: The final merged dict
    :rtype: dict
    """
    if keyisset("ACLs", override):
        override_acls = ACLs.parse_obj(override["ACLs"]).dict()
        if keypresent("Policies", override_acls) and not extend_all:
            del override_acls["Policies"]
            final["ACLs"].update(override_acls)
        elif keyisset("Policies", override_acls) and extend_all:
            if keyisset("Policies", final["ACLs"]):
                merged_lists = override_acls["Policies"] + final["ACLs"]["Policies"]
            else:
                merged_lists = override_acls["Policies"]
            acls = [dict(y) for y in set(tuple(x.items()) for x in merged_lists)]
            final["ACLs"].update(override_acls)
            final["ACLs"]["Policies"] = acls


def merge_contents(primary, override, extend_all=False):
    """
    Function to override and update settings from override to primary
    :param primary:
    :param override:
    :param extend_all: Whether the policies or ACLs can be merged.
    :return: The final merged dict
    :rtype: dict
    """
    if not isinstance(override, dict):
        raise TypeError(
            "The content of the override file does not match the expected content pattern."
        )
    final = dict(deepcopy(primary))
    if (
        keypresent("Globals", final)
        and keyisset("Globals", override)
        and isinstance(override["Globals"], dict)
    ):
        override_globals = EwsKafkaParmeters.parse_obj(override["Globals"])
        final["Globals"].update(override_globals.dict())

    merge_acls(final, override, extend_all)
    merge_topics(final, override, extend_all)
    return final


class KafkaStack(object):
    """
    Class to represent the Kafka topics / acls / schemas in CloudFormation.
    """

    def __init__(self, files_paths, config_file_path=None):
        self.model = None
        self.template = Template("Kafka topics-acls-schemas root")
        self.stack = None
        self.topic_class = RTopic
        self.acl_class = RACLs
        self.topics_r = {}
        self.globals_config = {}
        final_content = {"Globals": {}, "Topics": {}, "ACLs": {}}
        for file_path in files_paths:
            if file_path.endswith(".yaml") or file_path.endswith(".yml"):
                with open(file_path, "r") as file_fd:
                    file_content = file_fd.read()
                yaml_content = yaml.load(file_content, Loader=CfnYamlLoader)
                final_content = merge_contents(
                    final_content, yaml_content, extend_all=True
                )
        if config_file_path:
            with open(config_file_path, "r") as override_fd:
                override_content = override_fd.read()
            override_content = yaml.load(override_content, Loader=CfnYamlLoader)
            final_content = merge_contents(final_content, override_content)
        self.model = Model.parse_obj(final_content)

        if not self.model.Topics and not self.model.ACLs:
            raise KeyError("You must define at least one of ACLs or Topics")
        self.set_globals()

    def set_globals(self):
        """
        Method to set the global settings
        """
        self.globals_config.update(
            {
                "BootstrapServers": self.model.Globals.BootstrapServers,
                "SASLUsername": self.model.Globals.SASLUsername
                if self.model.Globals.SASLUsername
                else Ref(AWS_NO_VALUE),
                "SASLPassword": self.model.Globals.SASLPassword
                if self.model.Globals.SASLPassword
                else Ref(AWS_NO_VALUE),
                "SASLMechanism": SASLMechanism[
                    self.model.Globals.SASLMechanism.name
                ].value
                if isinstance(self.model.Globals.SASLMechanism, SASLMechanism)
                else self.model.Globals.SASLMechanism,
                "SecurityProtocol": SecurityProtocol[
                    self.model.Globals.SecurityProtocol.name
                ].value
                if isinstance(self.model.Globals.SecurityProtocol, SecurityProtocol)
                else self.model.Globals.SecurityProtocol,
            }
        )

    def render_topics(self):
        if not self.model.Topics or not self.model.Topics.Topics:
            print("No Topics defined")
            return
        function_name = None
        if self.model.Topics.FunctionName:
            self.topic_class = CTopic
            function_name = (
                function_name
                if self.model.Topics.FunctionName.startswith("arn:aws")
                else Sub(
                    "arn:${AWS::Partition}:lambda:${AWS::Region}:${AWS::AccountId}:function:"
                    f"{self.model.Topics.FunctionName}"
                )
            )
        for topic in self.model.Topics.Topics:
            topic_cfg = topic.dict()
            if function_name:
                topic_cfg.update({"ServiceToken": function_name})
            topic_cfg.update(self.globals_config)
            topic_cfg.update(
                {
                    "ReplicationFactor": self.model.Topics.ReplicationFactor.__root__
                    if not topic.ReplicationFactor
                    else topic.ReplicationFactor,
                }
            )
            if "Settings" in topic_cfg and not topic_cfg["Settings"]:
                del topic_cfg["Settings"]
            topic_r = self.template.add_resource(
                self.topic_class(NONALPHANUM.sub("", topic.Name), **topic_cfg)
            )
            self.topics_r[topic.Name] = topic_r

    def import_topic_name(self, policy):
        """
        Method to identify whether the resource provided is a topic referenced in the template

        :param Policy policy:
        :return:
        """
        if policy.ResourceType.value == ResourceType.TOPIC.name:
            topic_name = policy.Resource
            if topic_name in self.topics_r.keys():
                return GetAtt(self.topics_r[policy.Resource], "Name")
        return policy.Resource

    def render_acls(self):
        if not self.model.ACLs:
            return
        function_name = None
        if self.model.ACLs.FunctionName:
            self.acl_class = CACLs
            function_name = (
                function_name
                if self.model.ACLs.FunctionName.startswith("arn:aws")
                else Sub(
                    "arn:${AWS::Partition}:lambda:${AWS::Region}:${AWS::AccountId}:function:"
                    f"{self.model.ACLs.FunctionName}"
                )
            )
        acl = {}
        acl.update(self.globals_config)
        if function_name:
            acl.update({"ServiceToken": function_name})

        policies = []
        for policy in self.model.ACLs.Policies:
            if isinstance(policy.PatternType, str):
                pattern_key = policy.PatternType
            else:
                pattern_key = policy.PatternType.name
            policies.append(
                KafkaAclPolicy(
                    Resource=self.import_topic_name(policy),
                    ResourceType=ResourceType[policy.ResourceType.name].value,
                    Principal=policy.Principal,
                    PatternType=PatternType[pattern_key].value,
                    Action=Action[policy.Action.name].value,
                    Effect=Effect[policy.Effect.name].value,
                    Host=policy.Host if policy.Host else r"*",
                )
            )
        self.template.add_resource(self.acl_class("ACLs", Policies=policies, **acl))
