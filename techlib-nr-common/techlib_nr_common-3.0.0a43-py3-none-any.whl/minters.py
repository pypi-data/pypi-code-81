# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Persistent identifier minters."""

from __future__ import absolute_import, print_function

from invenio_pidstore.errors import PIDDoesNotExistError

from nr_common.providers import NRIdProvider


def nr_id_minter(record_uuid, data, nr_id_provider):
    """Mint record identifiers.

    This is a minter specific for records.
    With the help of
    :class:`invenio_pidstore.providers.recordid.RecordIdProvider`, it creates
    the PID instance with `rec` as predefined `object_type`.

    Procedure followed: (we will use `control_number` as value of
    `PIDSTORE_nr_id_FIELD` for the simplicity of the documentation.)

    #. If a `control_number` field is already there, a `AssertionError`
    exception is raised.

    #. The provider is initialized with the help of
    :class:`invenio_pidstore.providers.recordid.RecordIdProvider`.
    It's called with default value 'rec' for `object_type` and `record_uuid`
    variable for `object_uuid`.

    #. The new `id_value` is stored inside `data` as `control_number` field.

    :param record_uuid: The record UUID.
    :param data: The record metadata.
    :returns: A fresh `invenio_pidstore.models.PersistentIdentifier` instance.
    """
    pid_field = "control_number"
    pid_type = get_pid_type(data)
    nr_id_provider.pid_type = pid_type
    if pid_field not in data:
        provider = nr_id_provider.create(
            object_type='rec', object_uuid=record_uuid)
        data[pid_field] = provider.pid.pid_value
    else:
        try:
            provider = nr_id_provider.get(pid_value=str(data[pid_field]))
        except PIDDoesNotExistError:
            provider = nr_id_provider.create(
                object_type='rec',
                object_uuid=record_uuid,
                pid_value=data[pid_field],
            )
            data[pid_field] = provider.pid.pid_value
    return provider.pid


def get_pid_type(data):
    resource_type_array = data.get("resourceType")
    resource_type_array = [_ for _ in resource_type_array if _["is_ancestor"] is False]
    if len(resource_type_array) != 1:
        raise Exception("Something unexpected happen, nusl should have one resource type")
    resource_type = resource_type_array[0]
    slug = resource_type["links"]["self"].split("/")[-1]
    return get_model_by_slug(slug)


def get_model_by_slug(slug):
    mapping = {
        "conference-materials": "nrevt",
        "exhibition-catalogues-and-guides": "nrevt",
        "business-trip-reports": "nrevt",
        "press-releases": "nrevt",
        "bachelor-theses": "nrthe",
        "master-theses": "nrthe",
        "rigorous-theses": "nrthe",
        "doctoral-theses": "nrthe",
        "post-doctoral-theses": "nrthe",
        "certified-methodologies": "nrnrs",
        "preservation-procedures": "nrnrs",
        "specialized-maps": "nrnrs",
    }
    return mapping.get(slug, "nrcom")
