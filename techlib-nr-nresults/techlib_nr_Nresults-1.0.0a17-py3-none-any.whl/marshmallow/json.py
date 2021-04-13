# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""
from nr_common.marshmallow.fields import DateString
from nr_common.marshmallow.json import CommonMetadataSchemaV2
from nr_common.marshmallow.subschemas import TitledMixin
from invenio_records_rest.schemas.fields import SanitizedUnicode
from marshmallow.validate import Length
from oarepo_taxonomies.marshmallow import TaxonomyField

from nr_nresults.marshmallow.subschemas import NcertifyingAuthorityMixin


class NResultsMetadataSchemaV1(CommonMetadataSchemaV2):
    N_certifyingAuthority = TaxonomyField(mixins=[TitledMixin, NcertifyingAuthorityMixin])
    N_dateCertified = DateString()
    N_economicalParameters = SanitizedUnicode(validate=Length(max=1024))
    N_internalID = SanitizedUnicode()
    N_referenceNumber = SanitizedUnicode()
    N_resultUsage = TaxonomyField(mixins=[TitledMixin])
    N_technicalParameters = SanitizedUnicode(validate=Length(max=3000))
    N_type = TaxonomyField(mixins=[TitledMixin], required=True)
