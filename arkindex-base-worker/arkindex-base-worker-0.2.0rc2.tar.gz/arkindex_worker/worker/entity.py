# -*- coding: utf-8 -*-


from enum import Enum

from arkindex_worker import logger
from arkindex_worker.models import Element


class EntityType(Enum):
    Person = "person"
    Location = "location"
    Subject = "subject"
    Organization = "organization"
    Misc = "misc"
    Number = "number"
    Date = "date"


class EntityMixin(object):
    def create_entity(self, element, name, type, corpus, metas=None, validated=None):
        """
        Create an entity on the given corpus through API
        Return the ID of the created entity
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        assert name and isinstance(
            name, str
        ), "name shouldn't be null and should be of type str"
        assert type and isinstance(
            type, EntityType
        ), "type shouldn't be null and should be of type EntityType"
        assert corpus and isinstance(
            corpus, str
        ), "corpus shouldn't be null and should be of type str"
        if metas:
            assert isinstance(metas, dict), "metas should be of type dict"
        if validated is not None:
            assert isinstance(validated, bool), "validated should be of type bool"
        if self.is_read_only:
            logger.warning("Cannot create entity as this worker is in read-only mode")
            return

        entity = self.request(
            "CreateEntity",
            body={
                "name": name,
                "type": type.value,
                "metas": metas,
                "validated": validated,
                "corpus": corpus,
                "worker_version": self.worker_version_id,
            },
        )
        self.report.add_entity(element.id, entity["id"], type.value, name)

        return entity["id"]
