# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Persistent identifier minters."""

from __future__ import absolute_import, print_function

from nr_common.minters import nr_id_minter

from nr_theses.providers import NRThesesIdProvider


def nr_theses_id_minter(record_uuid, data):
    return nr_id_minter(record_uuid, data, nr_id_provider=NRThesesIdProvider)
