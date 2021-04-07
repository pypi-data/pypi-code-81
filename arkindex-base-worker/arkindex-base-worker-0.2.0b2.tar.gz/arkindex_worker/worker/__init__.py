# -*- coding: utf-8 -*-
import json
import os
import sys
import uuid
from enum import Enum

from apistar.exceptions import ErrorResponse

from arkindex_worker import logger
from arkindex_worker.cache import CachedElement
from arkindex_worker.models import Element
from arkindex_worker.reporting import Reporter
from arkindex_worker.worker.base import BaseWorker
from arkindex_worker.worker.classification import ClassificationMixin
from arkindex_worker.worker.element import ElementMixin
from arkindex_worker.worker.entity import EntityMixin, EntityType  # noqa: F401
from arkindex_worker.worker.metadata import MetaDataMixin, MetaType  # noqa: F401
from arkindex_worker.worker.transcription import TranscriptionMixin
from arkindex_worker.worker.version import WorkerVersionMixin  # noqa: F401


class ActivityState(Enum):
    Queued = "queued"
    Started = "started"
    Processed = "processed"
    Error = "error"


class ElementsWorker(
    BaseWorker,
    ClassificationMixin,
    ElementMixin,
    TranscriptionMixin,
    WorkerVersionMixin,
    EntityMixin,
    MetaDataMixin,
):
    def __init__(self, description="Arkindex Elements Worker", use_cache=False):
        super().__init__(description, use_cache)

        # Add report concerning elements
        self.report = Reporter("unknown worker")

        # Add mandatory argument to process elements
        self.parser.add_argument(
            "--elements-list",
            help="JSON elements list to use",
            type=open,
            default=os.environ.get("TASK_ELEMENTS"),
        )
        self.parser.add_argument(
            "--element",
            type=uuid.UUID,
            nargs="+",
            help="One or more Arkindex element ID",
        )
        self.classes = {}

        self._worker_version_cache = {}

    def list_elements(self):
        assert not (
            self.args.elements_list and self.args.element
        ), "elements-list and element CLI args shouldn't be both set"
        out = []

        # Load from the cache when available
        # Flake8 wants us to use 'is True', but Peewee only supports '== True'
        cache_query = CachedElement.select().where(
            CachedElement.initial == True  # noqa: E712
        )
        if self.use_cache and cache_query.exists():
            return cache_query
        # Process elements from JSON file
        elif self.args.elements_list:
            data = json.load(self.args.elements_list)
            assert isinstance(data, list), "Elements list must be a list"
            assert len(data), "No elements in elements list"
            out += list(filter(None, [element.get("id") for element in data]))
        # Add any extra element from CLI
        elif self.args.element:
            out += self.args.element

        return out

    def run(self):
        """
        Process every elements from the provided list
        """
        self.configure()

        # List all elements either from JSON file
        # or direct list of elements on CLI
        elements = self.list_elements()
        if not elements:
            logger.warning("No elements to process, stopping.")
            sys.exit(1)

        # Process every element
        count = len(elements)
        failed = 0
        for i, item in enumerate(elements, start=1):
            element = None
            try:
                if self.use_cache:
                    # Just use the result of list_elements as the element
                    element = item
                else:
                    # Load element using the Arkindex API
                    element = Element(**self.request("RetrieveElement", id=item))

                logger.info(f"Processing {element} ({i}/{count})")

                # Report start of process, run process, then report end of process
                self.update_activity(element.id, ActivityState.Started)
                self.process_element(element)
                self.update_activity(element.id, ActivityState.Processed)
            except Exception as e:
                failed += 1
                element_id = (
                    element.id
                    if isinstance(element, (Element, CachedElement))
                    else item
                )

                if isinstance(e, ErrorResponse):
                    message = f"An API error occurred while processing element {element_id}: {e.title} - {e.content}"
                else:
                    message = f"Failed running worker on element {element_id}: {e}"

                logger.warning(
                    message,
                    exc_info=e if self.args.verbose else None,
                )
                self.update_activity(element_id, ActivityState.Error)
                self.report.error(element_id, e)

        # Save report as local artifact
        self.report.save(os.path.join(self.work_dir, "ml_report.json"))

        if failed:
            logger.error(
                "Ran on {} elements: {} completed, {} failed".format(
                    count, count - failed, failed
                )
            )
            if failed >= count:  # Everything failed!
                sys.exit(1)

    def process_element(self, element):
        """Override this method to analyze an Arkindex element from the provided list"""

    def update_activity(self, element_id, state):
        """
        Update worker activity for this element
        This method should not raise a runtime exception, but simply warn users
        """
        assert element_id and isinstance(
            element_id, (uuid.UUID, str)
        ), "element_id shouldn't be null and should be an UUID or str"
        assert isinstance(state, ActivityState), "state should be an ActivityState"

        if not self.features.get("workers_activity"):
            logger.debug("Skipping Worker activity update as it's disabled on backend")
            return

        if self.is_read_only:
            logger.warning("Cannot update activity as this worker is in read-only mode")
            return

        try:
            out = self.request(
                "UpdateWorkerActivity",
                id=self.worker_version_id,
                body={
                    "element_id": str(element_id),
                    "state": state.value,
                },
            )
            logger.debug(f"Updated activity of element {element_id} to {state}")
            return out
        except ErrorResponse as e:
            logger.warning(
                f"Failed to update activity of element {element_id} to {state.value} due to an API error: {e.content}"
            )
        except Exception as e:
            logger.warning(
                f"Failed to update activity of element {element_id} to {state.value}: {e}"
            )
