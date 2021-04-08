# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Thesis ID provider."""

from __future__ import absolute_import, print_function

from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.models import PIDStatus, PersistentIdentifier
from invenio_pidstore.providers.base import BaseProvider

from nr_common.models import NRIdentifier


class NRIdProvider(BaseProvider):
    """Thesss identifier provider."""

    pid_type = 'nrcom'
    """Type of persistent identifier."""

    pid_provider = None
    """Provider name.

    The provider name is not recorded in the PID since the provider does not
    provide any additional features besides creation of record ids.
    """

    default_status = PIDStatus.RESERVED
    """Record IDs are by default registered immediately.

    Default: :attr:`invenio_pidstore.models.PIDStatus.RESERVED`
    """

    @classmethod
    def create(cls, object_type=None, object_uuid=None, **kwargs):
        """Create a new record identifier.

        Note: if the object_type and object_uuid values are passed, then the
        PID status will be automatically setted to
        :attr:`invenio_pidstore.models.PIDStatus.REGISTERED`.

        :param object_type: The object type. (Default: None.)
        :param object_uuid: The object identifier. (Default: None).
        :param kwargs: You specify the pid_value.
        """
        # Request next integer in recid sequence.
        if 'pid_value' not in kwargs:
            kwargs['pid_value'] = str(NRIdentifier.next())
        else:
            NRIdentifier.insert(kwargs['pid_value'])
        kwargs.setdefault('status', cls.default_status)
        if object_type and object_uuid:
            kwargs['status'] = PIDStatus.REGISTERED
        return super(NRIdProvider, cls).create(
            object_type=object_type, object_uuid=object_uuid, **kwargs)

    @classmethod
    def get(cls, pid_value, pid_type=None, **kwargs):
        """Get a persistent identifier for this provider.

        :param pid_type: Persistent identifier type. (Default: configured
            :attr:`invenio_pidstore.providers.base.BaseProvider.pid_type`)
        :param pid_value: Persistent identifier value.
        :param kwargs: See
            :meth:`invenio_pidstore.providers.base.BaseProvider` required
            initialization properties.
        :returns: A :class:`invenio_pidstore.providers.base.BaseProvider`
            instance.
        """
        try:
            pid = PersistentIdentifier.get(pid_type or cls.pid_type, pid_value,
                                       pid_provider=cls.pid_provider)
        except PIDDoesNotExistError:
            pid_type = pid_type or cls.pid_type
            pid_type = "d" + pid_type
            pid = PersistentIdentifier.get(pid_type or cls.pid_type, pid_value,
                                           pid_provider=cls.pid_provider)
        return cls(
            pid,
            **kwargs)

