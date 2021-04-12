from __future__ import annotations

from media_platform.job.job import Job
from media_platform.job.job_type import JobType
from media_platform.job.specification import Specification


class IndexImageSpecification(Specification):
    @classmethod
    def deserialize(cls, data):
        return IndexImageSpecification()

    def serialize(self) -> dict:
        return {}


class IndexImageJob(Job):
    type = JobType.index_image
    specification_type = IndexImageSpecification
