# -*- coding: utf-8 -*-

from peewee import IntegrityError

from arkindex_worker import logger
from arkindex_worker.cache import CachedElement, CachedTranscription
from arkindex_worker.models import Element


class TranscriptionMixin(object):
    def create_transcription(self, element, text, score):
        """
        Create a transcription on the given element through the API.
        """
        assert element and isinstance(
            element, (Element, CachedElement)
        ), "element shouldn't be null and should be an Element or CachedElement"
        assert text and isinstance(
            text, str
        ), "text shouldn't be null and should be of type str"

        assert (
            isinstance(score, float) and 0 <= score <= 1
        ), "score shouldn't be null and should be a float in [0..1] range"

        if self.is_read_only:
            logger.warning(
                "Cannot create transcription as this worker is in read-only mode"
            )
            return

        created = self.request(
            "CreateTranscription",
            id=element.id,
            body={
                "text": text,
                "worker_version": self.worker_version_id,
                "score": score,
            },
        )

        self.report.add_transcription(element.id)

        if self.use_cache:
            # Store transcription in local cache
            try:
                to_insert = [
                    {
                        "id": created["id"],
                        "element_id": element.id,
                        "text": created["text"],
                        "confidence": created["confidence"],
                        "worker_version_id": self.worker_version_id,
                    }
                ]
                CachedTranscription.insert_many(to_insert).execute()
            except IntegrityError as e:
                logger.warning(
                    f"Couldn't save created transcription in local cache: {e}"
                )

    def create_transcriptions(self, transcriptions):
        """
        Create multiple transcriptions at once on existing elements through the API.
        """

        assert transcriptions and isinstance(
            transcriptions, list
        ), "transcriptions shouldn't be null and should be of type list"

        for index, transcription in enumerate(transcriptions):
            element_id = transcription.get("element_id")
            assert element_id and isinstance(
                element_id, str
            ), f"Transcription at index {index} in transcriptions: element_id shouldn't be null and should be of type str"

            text = transcription.get("text")
            assert text and isinstance(
                text, str
            ), f"Transcription at index {index} in transcriptions: text shouldn't be null and should be of type str"

            score = transcription.get("score")
            assert (
                score is not None and isinstance(score, float) and 0 <= score <= 1
            ), f"Transcription at index {index} in transcriptions: score shouldn't be null and should be a float in [0..1] range"

        created_trs = self.request(
            "CreateTranscriptions",
            body={
                "worker_version": self.worker_version_id,
                "transcriptions": transcriptions,
            },
        )["transcriptions"]

        for created_tr in created_trs:
            self.report.add_transcription(created_tr["element_id"])

        if self.use_cache:
            # Store transcriptions in local cache
            try:
                to_insert = [
                    {
                        "id": created_tr["id"],
                        "element_id": created_tr["element_id"],
                        "text": created_tr["text"],
                        "confidence": created_tr["confidence"],
                        "worker_version_id": self.worker_version_id,
                    }
                    for created_tr in created_trs
                ]
                CachedTranscription.insert_many(to_insert).execute()
            except IntegrityError as e:
                logger.warning(
                    f"Couldn't save created transcriptions in local cache: {e}"
                )

    def create_element_transcriptions(self, element, sub_element_type, transcriptions):
        """
        Create multiple sub elements with their transcriptions on the given element through API
        """
        assert element and isinstance(
            element, (Element, CachedElement)
        ), "element shouldn't be null and should be an Element or CachedElement"
        assert sub_element_type and isinstance(
            sub_element_type, str
        ), "sub_element_type shouldn't be null and should be of type str"
        assert transcriptions and isinstance(
            transcriptions, list
        ), "transcriptions shouldn't be null and should be of type list"

        for index, transcription in enumerate(transcriptions):
            text = transcription.get("text")
            assert text and isinstance(
                text, str
            ), f"Transcription at index {index} in transcriptions: text shouldn't be null and should be of type str"

            score = transcription.get("score")
            assert (
                score is not None and isinstance(score, float) and 0 <= score <= 1
            ), f"Transcription at index {index} in transcriptions: score shouldn't be null and should be a float in [0..1] range"

            polygon = transcription.get("polygon")
            assert polygon and isinstance(
                polygon, list
            ), f"Transcription at index {index} in transcriptions: polygon shouldn't be null and should be of type list"
            assert (
                len(polygon) >= 3
            ), f"Transcription at index {index} in transcriptions: polygon should have at least three points"
            assert all(
                isinstance(point, list) and len(point) == 2 for point in polygon
            ), f"Transcription at index {index} in transcriptions: polygon points should be lists of two items"
            assert all(
                isinstance(coord, (int, float)) for point in polygon for coord in point
            ), f"Transcription at index {index} in transcriptions: polygon points should be lists of two numbers"
        if self.is_read_only:
            logger.warning(
                "Cannot create transcriptions as this worker is in read-only mode"
            )
            return

        annotations = self.request(
            "CreateElementTranscriptions",
            id=element.id,
            body={
                "element_type": sub_element_type,
                "worker_version": self.worker_version_id,
                "transcriptions": transcriptions,
                "return_elements": True,
            },
        )

        for annotation in annotations:
            if annotation["created"]:
                logger.debug(
                    f"A sub_element of {element.id} with type {sub_element_type} was created during transcriptions bulk creation"
                )
                self.report.add_element(element.id, sub_element_type)
            self.report.add_transcription(annotation["element_id"])

        if self.use_cache:
            # Store transcriptions and their associated element (if created) in local cache
            created_ids = set()
            elements_to_insert = []
            transcriptions_to_insert = []
            for index, annotation in enumerate(annotations):
                transcription = transcriptions[index]

                if annotation["element_id"] not in created_ids:
                    # Even if the API says the element already existed in the DB,
                    # we need to check if it is available in the local cache.
                    # Peewee does not have support for SQLite's INSERT OR IGNORE,
                    # so we do the check here, element by element.
                    try:
                        CachedElement.get_by_id(annotation["element_id"])
                    except CachedElement.DoesNotExist:
                        elements_to_insert.append(
                            {
                                "id": annotation["element_id"],
                                "parent_id": element.id,
                                "type": sub_element_type,
                                "image_id": element.image_id,
                                "polygon": transcription["polygon"],
                                "worker_version_id": self.worker_version_id,
                            }
                        )

                    created_ids.add(annotation["element_id"])

                transcriptions_to_insert.append(
                    {
                        "id": annotation["id"],
                        "element_id": annotation["element_id"],
                        "text": transcription["text"],
                        "confidence": transcription["score"],
                        "worker_version_id": self.worker_version_id,
                    }
                )

            try:
                CachedElement.insert_many(elements_to_insert).execute()
                CachedTranscription.insert_many(transcriptions_to_insert).execute()
            except IntegrityError as e:
                logger.warning(
                    f"Couldn't save created transcriptions in local cache: {e}"
                )

        return annotations

    def list_transcriptions(
        self, element, element_type=None, recursive=None, worker_version=None
    ):
        """
        List transcriptions on an element
        """
        assert element and isinstance(
            element, (Element, CachedElement)
        ), "element shouldn't be null and should be an Element or CachedElement"
        query_params = {}
        if element_type:
            assert isinstance(element_type, str), "element_type should be of type str"
            query_params["element_type"] = element_type
        if recursive is not None:
            assert isinstance(recursive, bool), "recursive should be of type bool"
            query_params["recursive"] = recursive
        if worker_version:
            assert isinstance(
                worker_version, str
            ), "worker_version should be of type str"
            query_params["worker_version"] = worker_version

        if self.use_cache and recursive is None:
            # Checking that we only received query_params handled by the cache
            assert set(query_params.keys()) <= {
                "worker_version",
            }, "When using the local cache, you can only filter by 'worker_version'"

            transcriptions = CachedTranscription.select().where(
                CachedTranscription.element_id == element.id
            )
            if worker_version:
                transcriptions = transcriptions.where(
                    CachedTranscription.worker_version_id == worker_version
                )
        else:
            if self.use_cache:
                logger.warning(
                    "'recursive' filter was set, results will be retrieved from the API since the local cache doesn't handle this filter."
                )
            transcriptions = self.api_client.paginate(
                "ListTranscriptions", id=element.id, **query_params
            )

        return transcriptions
