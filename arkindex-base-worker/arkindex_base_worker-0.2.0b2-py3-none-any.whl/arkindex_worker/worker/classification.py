# -*- coding: utf-8 -*-
from apistar.exceptions import ErrorResponse

from arkindex_worker import logger
from arkindex_worker.models import Element


class ClassificationMixin(object):
    def load_corpus_classes(self, corpus_id):
        """
        Load ML classes for the given corpus ID
        """
        corpus_classes = self.api_client.paginate(
            "ListCorpusMLClasses",
            id=corpus_id,
        )
        self.classes[corpus_id] = {
            ml_class["name"]: ml_class["id"] for ml_class in corpus_classes
        }
        logger.info(f"Loaded {len(self.classes[corpus_id])} ML classes")

    def get_ml_class_id(self, corpus_id, ml_class):
        """
        Return the ID corresponding to the given class name on a specific corpus
        This method will automatically create missing classes
        """
        if not self.classes.get(corpus_id):
            self.load_corpus_classes(corpus_id)

        ml_class_id = self.classes[corpus_id].get(ml_class)
        if ml_class_id is None:
            logger.info(f"Creating ML class {ml_class} on corpus {corpus_id}")
            try:
                response = self.request(
                    "CreateMLClass", id=corpus_id, body={"name": ml_class}
                )
                ml_class_id = self.classes[corpus_id][ml_class] = response["id"]
                logger.debug(f"Created ML class {response['id']}")
            except ErrorResponse as e:
                # Only reload for 400 errors
                if e.status_code != 400:
                    raise

                # Reload and make sure we have the class
                logger.info(
                    f"Reloading corpus classes to see if {ml_class} already exists"
                )
                self.load_corpus_classes(corpus_id)
                assert (
                    ml_class in self.classes[corpus_id]
                ), "Missing class {ml_class} even after reloading"
                ml_class_id = self.classes[corpus_id][ml_class]

        return ml_class_id

    def create_classification(
        self, element, ml_class, confidence, high_confidence=False
    ):
        """
        Create a classification on the given element through API
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        assert ml_class and isinstance(
            ml_class, str
        ), "ml_class shouldn't be null and should be of type str"
        assert (
            isinstance(confidence, float) and 0 <= confidence <= 1
        ), "confidence shouldn't be null and should be a float in [0..1] range"
        assert isinstance(
            high_confidence, bool
        ), "high_confidence shouldn't be null and should be of type bool"
        if self.is_read_only:
            logger.warning(
                "Cannot create classification as this worker is in read-only mode"
            )
            return

        try:
            self.request(
                "CreateClassification",
                body={
                    "element": element.id,
                    "ml_class": self.get_ml_class_id(element.corpus.id, ml_class),
                    "worker_version": self.worker_version_id,
                    "confidence": confidence,
                    "high_confidence": high_confidence,
                },
            )
        except ErrorResponse as e:

            # Detect already existing classification
            if (
                e.status_code == 400
                and "non_field_errors" in e.content
                and "The fields element, worker_version, ml_class must make a unique set."
                in e.content["non_field_errors"]
            ):
                logger.warning(
                    f"This worker version has already set {ml_class} on element {element.id}"
                )
                return

            # Propagate any other API error
            raise

        self.report.add_classification(element.id, ml_class)
