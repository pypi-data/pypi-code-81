# !/usr/bin/env python
# -*- coding:utf-8 -*-

import pathlib as pt
import logging as log

from fameio.source.AttributeValidator import AttributeValidator, AttributeType
from fameio.source.TimeSeriesManager import TimeSeriesManager
from fameio.source.tools import arg_handling_make_config, get_valid_key, log_and_raise, set_up_logger
from fameio.source.loader import load_yaml
from fameio.source.FameTime import FameTime
from fameprotobuf import InputFile_pb2
from fameprotobuf import Contract_pb2
from fameprotobuf import DataStorage_pb2


DEFAULT_CONFIG = {"log_level": "warning",
                  "output_file": "config.pb",
                  "log_file": None,
                  }


def set_general_properties(properties, proto):
    """Set the general properties in the given protobuf"""
    valid_keys = [field.name for field in InputFile_pb2._INPUTDATA.fields]
    for property_name, property_value in properties.items():
        property_name = get_valid_key(property_name, valid_keys)
        if not hasattr(property_value, "keys"):
            setattr(proto, property_name, property_value)
        else:
            parent = getattr(proto, property_name)
            valid_child_keys = parent.DESCRIPTOR.fields_by_name.keys()
            for child_property_name, child_property_value in property_value.items():
                child_property_name = get_valid_key(child_property_name, valid_child_keys)
                child_property_value = convert_string_if_is_datetime(child_property_value)
                setattr(parent, child_property_name, child_property_value)
        log.info("Set general properties for `{}`".format(property_name))


def convert_string_if_is_datetime(value):
    """Returns given `value` in FameTime steps if it is DateTime string, otherwise returns `value`"""
    if FameTime.is_datetime(value):
        value = int(FameTime.convert_datetime_to_fame_time_step(value))
    return value


def set_attributes(pb_agent, attributes, time_series_manager, validator):
    """Adds all attributes in the given list to the given agent proto buffer"""
    if attributes is None:
        return

    assign_agent_attributes(pb_agent.className, list(), pb_agent, attributes, validator, time_series_manager)


def assign_agent_attributes(agent_type, parent_locator, pb_parent, attributes, validator, time_series_manager):
    """Assigns agent attributes to protobuf fields on this level and calls `assign_attributes()` for nested elements"""
    for attribute_name, attribute_value in attributes.items():
        pb_field = pb_parent.field.add()
        pb_field.fieldName = attribute_name
        attribute_locator = parent_locator.copy()
        attribute_locator.append(attribute_name)
        attribute_type = validator.get_attribute_type(agent_type, attribute_locator)

        if validator.is_valid(agent_type, attribute_locator, attribute_value):
            if attribute_type is AttributeType.INTEGER:
                pb_field.intValue = attribute_value
            elif attribute_type is AttributeType.DOUBLE:
                pb_field.doubleValue.extend([attribute_value])
            elif attribute_type is AttributeType.ENUM:
                pb_field.stringValue = attribute_value
            elif attribute_type is AttributeType.TIME_SERIES:
                set_time_series_from_value(attribute_value, pb_field, time_series_manager)
            elif attribute_type is AttributeType.DOUBLE_LIST:
                set_double_list_from_value(attribute_value, pb_field)
            elif attribute_type is AttributeType.BLOCK:
                assign_agent_attributes(agent_type=agent_type,
                                        parent_locator=attribute_locator,
                                        pb_parent=pb_field,
                                        attributes=attribute_value,
                                        validator=validator,
                                        time_series_manager=time_series_manager)
            else:
                log_and_raise("AttributeType '{}' not implemented.".format(attribute_type))
        else:
            log_and_raise(
                "'{}' not allowed in attribute '{}' of agent {}".format(attribute_value, attribute_name, agent_type))


def assign_contract_attributes(pb_parent, attributes):
    """Assign contract attributes to protobuf nested field"""
    for attribute_name, attribute_value in attributes.items():
        log.debug("Assigning contract attribute `{}`.".format(attribute_name))
        pb_field = pb_parent.field.add()
        pb_field.fieldName = attribute_name

        if isinstance(attribute_value, int):
            pb_field.intValue = attribute_value
        elif isinstance(attribute_value, float):
            pb_field.doubleValue.extend([attribute_value])
        elif isinstance(attribute_value, str):
            pb_field.stringValue = attribute_value
        elif isinstance(attribute_value, dict):
            assign_contract_attributes(pb_field, attribute_value)
        else:
            log_and_raise("Contract attributes only support `int`, `float`, `enum` or `dict` types.")


def set_double_list_from_value(value_list, pb_field):
    """Sets given double value list `value_list` to `pb_field`.doubleValue"""
    for element in value_list:
        pb_field.doubleValue.extend([element])


def set_time_series_from_value(value, pb_field, time_series_manager):
    """Hands given `value` to `time_series_manager` to assign a time series id which is set to `pb_field`.seriesId"""
    if isinstance(value, str):
        file_name = pt.Path(value).as_posix()
        pb_field.seriesId = time_series_manager.save_get_time_series_id(file_name)
    else:
        pb_field.seriesId = time_series_manager.save_get_time_series_id(value)


def get_or_error(dict: dict, key):
    """Gets given `key` from `dict` or raises error if `key` is missing"""
    try:
        return dict[key]
    except KeyError:
        log_and_raise("Cannot find '{}' in dict {}.".format(key, dict))


def set_agents_and_time_series(agent_list, proto_buffer, validator):
    """
    Iterates through all agents, adds them and all of their attributes to the given proto buffer and also
    adds all referenced files as time series to the proto_buffer. Ensures proper attribute parameterization and format.
    """
    time_series_manager = TimeSeriesManager()
    for agent in agent_list:
        agent = convert_keys_to_lower(agent)
        pb_agent = proto_buffer.agent.add()
        pb_agent.className = get_or_error(agent, "type")
        pb_agent.id = get_or_error(agent, "id")
        if "attributes" in agent:
            attributes = agent.get("attributes")
            set_attributes(pb_agent, attributes, time_series_manager, validator)
        log.info("Set `Attributes` for agent `{}` with ID `{}`".format(pb_agent.className, pb_agent.id))
    time_series_manager.add_time_series_to_proto_buffer(proto_buffer)


def convert_keys_to_lower(agent):
    """Returns given dictionary with `keys` in lower case"""
    return {keys.lower(): value for keys, value in agent.items()}


def set_contracts(agents, schema, contracts, proto_buffer):
    """Adds `contracts` to `proto_buffer` and checks if product is valid according to `agent`s products in `schema` """
    agent_type_by_id = get_agent_type_by_id(agents)
    valid_keys = [field.name for field in Contract_pb2._PROTOCONTRACT.fields]

    for contract in contracts:
        check_for_valid_product(agent_type_by_id, schema, contract)

        pb_contract = proto_buffer.contract.add()
        for key, value in contract.items():
            if key.lower() == "attributes":
                if value:
                    assign_contract_attributes(pb_contract, value)
            else:
                key = get_valid_key(key, valid_keys)
                value = convert_string_if_is_datetime(value)
                setattr(pb_contract, key, value)

    log.info("Added contracts to protobuf file.")


def check_for_valid_product(agent_type_by_id, schema, contract):
    """Raises error if invalid `product` is specified in `contract` according to provided `schema`"""
    sender = agent_type_by_id[contract['SenderId']]
    valid_products = schema['AgentTypes'][sender]['Products']
    if contract['ProductName'] not in valid_products:
        log_and_raise("Invalid product defined in contract `{}`. "
                      "Valid products are `{}`.".format(contract, valid_products))


def get_agent_type_by_id(agents):
    """Returns dict of `agents` with key `Id` and value `Type`"""
    agent_type_by_id = dict()
    for agent in agents:
        agent_type_by_id[agent['Id']] = agent['Type']
    return agent_type_by_id


def write_protobuf_to_disk(output_file, proto_input_data):
    """Writes given `protobuf_input_data` in `output_file` to disk"""
    f = open(output_file, "wb")
    f.write(proto_input_data.SerializeToString())
    f.close()
    log.info("Saved protobuf file `{}` to disk".format(output_file))


def run(file, config=DEFAULT_CONFIG):
    """Executes the main workflow for the building of a FAME configuration file"""
    set_up_logger(level=config["log_level"], file_name=config["log_file"])

    config_data = load_yaml(file)
    validator = AttributeValidator(config_data["Schema"])

    proto_data_storage = DataStorage_pb2.DataStorage()
    proto_input_data = proto_data_storage.input

    set_general_properties(config_data["GeneralProperties"], proto_input_data)
    set_agents_and_time_series(config_data["Agents"], proto_input_data, validator)
    set_contracts(config_data["Agents"], config_data["Schema"], config_data["Contracts"], proto_input_data)

    write_protobuf_to_disk(config["output_file"], proto_data_storage)

    log.info("Completed conversion of all input in `{}` to protobuf file `{}`".format(file, config["output_file"]))


if __name__ == '__main__':
    input_file, run_config = arg_handling_make_config(DEFAULT_CONFIG)
    run(input_file, run_config)
