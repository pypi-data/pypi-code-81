# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""This module defines the tests for the target utilities."""

from couplet_composer.util.target import \
    parse_target_from_argument_string, Target


def test_parse_target_from_argument_string():
    first = Target(system="MadeUpSystem", machine="x86_64")
    second = parse_target_from_argument_string("MadeUpSystem-x86_64")
    assert first == second
