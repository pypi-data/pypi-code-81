# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Thesis ID provider."""

from __future__ import absolute_import, print_function

from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.base import BaseProvider

from nr_common.models import NRIdentifier
from nr_common.providers import NRIdProvider


class NREventsIdProvider(NRIdProvider):
    pid_type = 'nrevt'
