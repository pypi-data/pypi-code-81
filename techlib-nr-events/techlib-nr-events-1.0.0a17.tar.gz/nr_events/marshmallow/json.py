# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from nr_common.marshmallow.json import CommonMetadataSchemaV2
from marshmallow.fields import List, Nested

from nr_events.marshmallow.subschemas import Events


class EventsMetadataSchemaV1(CommonMetadataSchemaV2):
    events = List(Nested(Events()))
