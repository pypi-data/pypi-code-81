# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""DataCite-based data model for Invenio."""

from invenio_indexer.api import RecordIndexer
from invenio_records_files.api import Record
from invenio_records_rest.facets import terms_filter
from invenio_records_rest.utils import allow_all
from invenio_search import RecordsSearch


def _(x):
    """Identity function for string extraction."""
    return x

#: Allow list of contributor types.
RECORD_CONTRIBUTOR_TYPES = [
    dict(label='Contact person', datacite='ContactPerson'),
    dict(label='Data collector', datacite='DataCollector'),
    dict(label='Data curator', datacite='DataCurator'),
    dict(label='Data manager', datacite='DataManager'),
    dict(label='Distributor', datacite='Distributor'),
    dict(label='Editor', datacite='Editor'),
    dict(label='Hosting institution', datacite='HostingInstitution'),
    dict(label='Other', datacite='Other'),
    dict(label='Producer', datacite='Producer'),
    dict(label='Project leader', datacite='ProjectLeader'),
    dict(label='Project manager', datacite='ProjectManager'),
    dict(label='Project member', datacite='ProjectMember'),
    dict(label='Registration agency', datacite='RegistrationAgency'),
    dict(label='Registration authority', datacite='RegistrationAuthority'),
    dict(label='Related person', datacite='RelatedPerson'),
    dict(label='Researcher', datacite='Researcher'),
    dict(label='Research group', datacite='ResearchGroup'),
    dict(label='Rights holder', datacite='RightsHolder'),
    dict(label='Sponsor', datacite='Sponsor'),
    dict(label='Supervisor', datacite='Supervisor'),
    dict(label='Work package leader', datacite='WorkPackageLeader'),
    dict(label='Other', datacite='Other')
]

RECORD_CONTRIBUTOR_TYPES_LABELS = {
    x['datacite']: x['label'] for x in RECORD_CONTRIBUTOR_TYPES
}

FORMATTER_BADGES_ALLOWED_TITLES = ['DOI', 'doi']
"""List of allowed titles in badges."""

FORMATTER_BADGES_TITLE_MAPPING = {'doi': 'DOI'}
"""Mapping of titles."""

# Invenio-RDM-Records
# ===================

RDM_RECORDS_LOCAL_DOI_PREFIXES = ['10.9999']
"""List  of locally managed DOI prefixes."""

RDM_RECORDS_METADATA_NAMESPACES = {}
"""Namespaces for fields *added* to the metadata schema.

Of the shape:

.. code-block:: python

    {
        '<prefix1>': {
            '@context': '<url>'
        },
        # ...
        '<prefixN>': {
            '@context': '<url>'
        }
    }

For example:

.. code-block:: python

    {
        'dwc': {
            '@context': 'http://rs.tdwg.org/dwc/terms/'
        },
        'z':{
            '@context': 'https://zenodo.org/terms'
        }
    }

Use :const:`invenio_rdm_records.config.RDM_RECORDS_METADATA_EXTENSIONS` to
define the added fields.

See :class:`invenio_rdm_records.metadata_extensions.MetadataExtensions` for
how this configuration variable is used.
"""

RDM_RECORDS_METADATA_EXTENSIONS = {}
"""Fields added to the metadata schema.

Of the shape:

.. code-block:: python

    {
        '<prefix1>:<field1>': {
            'elasticsearch': '<allowed elasticsearch type>'
            'marshmallow': '<allowed marshmallow type>'
        },
        # ...
        '<prefixN>:<fieldN>': {
            'elasticsearch': '<allowed elasticsearch type>'
            'marshmallow': '<allowed marshmallow type>'
        }
    }

For example:

.. code-block:: python

    {
        'dwc:family': {
            'elasticsearch': 'keyword',
            'marshmallow': SanitizedUnicode()
        },
        'dwc:behavior': {
            'elasticsearch': 'text',
            'marshmallow': SanitizedUnicode()
        },
        'z:department': {
            'elasticsearch': 'text',
            'marshmallow': SanitizedUnicode()
        }
    }

Use :const:`invenio_rdm_records.config.RDM_RECORDS_METADATA_NAMESPACES` to
define the prefixes.

See :class:`invenio_rdm_records.metadata_extensions.MetadataExtensions` for
allowed types and how this configuration variable is used.
"""
