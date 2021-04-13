from typing import Optional

from pulumi import ComponentResource, ResourceOptions

from data_engineering_pulumi_components.aws.landing_bucket import LandingBucket

from data_engineering_pulumi_components.aws.raw_history_bucket import RawHistoryBucket

from data_engineering_pulumi_components.aws.move_function import MoveObjectFunction

from ..utils import Tagger


class LandToHistoryPipeline(ComponentResource):
    def __init__(
        self,
        name: str,
        aws_arn_for_put_permission: str,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__(
            t="data-engineering-pulumi-components:pipelines:LandToHistoryPipeline",
            name=name,
            props=None,
            opts=opts,
        )

        self._landing_bucket = LandingBucket(
            resource_name=name,
            name=name,
            aws_arn_for_put_permission=aws_arn_for_put_permission,
            tags=None,
            opts=ResourceOptions(parent=self),
        )

        self._raw_history_bucket = RawHistoryBucket(
            resource_name=name,
            name=name,
            tags=None,
            opts=ResourceOptions(parent=self),
        )

        self._move_object_function = MoveObjectFunction(
            destination_bucket=self._raw_history_bucket,
            name=name,
            source_bucket=self._landing_bucket,
            opts=ResourceOptions(parent=self),
            tagger=Tagger(environment_name="dev"),
            # TODO set Tagger as parameter part of the landtohistorypipeline class
        )
