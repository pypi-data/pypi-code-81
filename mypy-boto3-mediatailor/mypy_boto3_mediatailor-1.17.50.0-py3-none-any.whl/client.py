"""
Main interface for mediatailor service client

Usage::

    ```python
    import boto3
    from mypy_boto3_mediatailor import MediaTailorClient

    client: MediaTailorClient = boto3.client("mediatailor")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_mediatailor.paginator import (
    GetChannelSchedulePaginator,
    ListChannelsPaginator,
    ListPlaybackConfigurationsPaginator,
    ListSourceLocationsPaginator,
    ListVodSourcesPaginator,
)
from mypy_boto3_mediatailor.type_defs import (
    AccessConfigurationTypeDef,
    AdBreakTypeDef,
    AvailSuppressionTypeDef,
    BumperTypeDef,
    CdnConfigurationTypeDef,
    CreateChannelResponseTypeDef,
    CreateProgramResponseTypeDef,
    CreateSourceLocationResponseTypeDef,
    CreateVodSourceResponseTypeDef,
    DashConfigurationForPutTypeDef,
    DefaultSegmentDeliveryConfigurationTypeDef,
    DescribeChannelResponseTypeDef,
    DescribeProgramResponseTypeDef,
    DescribeSourceLocationResponseTypeDef,
    DescribeVodSourceResponseTypeDef,
    GetChannelPolicyResponseTypeDef,
    GetChannelScheduleResponseTypeDef,
    GetPlaybackConfigurationResponseTypeDef,
    HttpConfigurationTypeDef,
    HttpPackageConfigurationTypeDef,
    ListChannelsResponseTypeDef,
    ListPlaybackConfigurationsResponseTypeDef,
    ListSourceLocationsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVodSourcesResponseTypeDef,
    LivePreRollConfigurationTypeDef,
    ManifestProcessingRulesTypeDef,
    PutPlaybackConfigurationResponseTypeDef,
    RequestOutputItemTypeDef,
    ScheduleConfigurationTypeDef,
    UpdateChannelResponseTypeDef,
    UpdateSourceLocationResponseTypeDef,
    UpdateVodSourceResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MediaTailorClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]


class MediaTailorClient:
    """
    [MediaTailor.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.can_paginate)
        """

    def create_channel(
        self,
        ChannelName: str,
        Outputs: List[RequestOutputItemTypeDef],
        PlaybackMode: Literal["LOOP"],
        Tags: Dict[str, str] = None,
    ) -> CreateChannelResponseTypeDef:
        """
        [Client.create_channel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.create_channel)
        """

    def create_program(
        self,
        ChannelName: str,
        ProgramName: str,
        ScheduleConfiguration: ScheduleConfigurationTypeDef,
        SourceLocationName: str,
        VodSourceName: str,
        AdBreaks: List["AdBreakTypeDef"] = None,
    ) -> CreateProgramResponseTypeDef:
        """
        [Client.create_program documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.create_program)
        """

    def create_source_location(
        self,
        HttpConfiguration: "HttpConfigurationTypeDef",
        SourceLocationName: str,
        AccessConfiguration: "AccessConfigurationTypeDef" = None,
        DefaultSegmentDeliveryConfiguration: "DefaultSegmentDeliveryConfigurationTypeDef" = None,
        Tags: Dict[str, str] = None,
    ) -> CreateSourceLocationResponseTypeDef:
        """
        [Client.create_source_location documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.create_source_location)
        """

    def create_vod_source(
        self,
        HttpPackageConfigurations: List["HttpPackageConfigurationTypeDef"],
        SourceLocationName: str,
        VodSourceName: str,
        Tags: Dict[str, str] = None,
    ) -> CreateVodSourceResponseTypeDef:
        """
        [Client.create_vod_source documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.create_vod_source)
        """

    def delete_channel(self, ChannelName: str) -> Dict[str, Any]:
        """
        [Client.delete_channel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.delete_channel)
        """

    def delete_channel_policy(self, ChannelName: str) -> Dict[str, Any]:
        """
        [Client.delete_channel_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.delete_channel_policy)
        """

    def delete_playback_configuration(self, Name: str) -> Dict[str, Any]:
        """
        [Client.delete_playback_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.delete_playback_configuration)
        """

    def delete_program(self, ChannelName: str, ProgramName: str) -> Dict[str, Any]:
        """
        [Client.delete_program documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.delete_program)
        """

    def delete_source_location(self, SourceLocationName: str) -> Dict[str, Any]:
        """
        [Client.delete_source_location documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.delete_source_location)
        """

    def delete_vod_source(self, SourceLocationName: str, VodSourceName: str) -> Dict[str, Any]:
        """
        [Client.delete_vod_source documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.delete_vod_source)
        """

    def describe_channel(self, ChannelName: str) -> DescribeChannelResponseTypeDef:
        """
        [Client.describe_channel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.describe_channel)
        """

    def describe_program(
        self, ChannelName: str, ProgramName: str
    ) -> DescribeProgramResponseTypeDef:
        """
        [Client.describe_program documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.describe_program)
        """

    def describe_source_location(
        self, SourceLocationName: str
    ) -> DescribeSourceLocationResponseTypeDef:
        """
        [Client.describe_source_location documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.describe_source_location)
        """

    def describe_vod_source(
        self, SourceLocationName: str, VodSourceName: str
    ) -> DescribeVodSourceResponseTypeDef:
        """
        [Client.describe_vod_source documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.describe_vod_source)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.generate_presigned_url)
        """

    def get_channel_policy(self, ChannelName: str) -> GetChannelPolicyResponseTypeDef:
        """
        [Client.get_channel_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.get_channel_policy)
        """

    def get_channel_schedule(
        self,
        ChannelName: str,
        DurationMinutes: str = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> GetChannelScheduleResponseTypeDef:
        """
        [Client.get_channel_schedule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.get_channel_schedule)
        """

    def get_playback_configuration(self, Name: str) -> GetPlaybackConfigurationResponseTypeDef:
        """
        [Client.get_playback_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.get_playback_configuration)
        """

    def list_channels(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListChannelsResponseTypeDef:
        """
        [Client.list_channels documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.list_channels)
        """

    def list_playback_configurations(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListPlaybackConfigurationsResponseTypeDef:
        """
        [Client.list_playback_configurations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.list_playback_configurations)
        """

    def list_source_locations(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListSourceLocationsResponseTypeDef:
        """
        [Client.list_source_locations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.list_source_locations)
        """

    def list_tags_for_resource(self, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.list_tags_for_resource)
        """

    def list_vod_sources(
        self, SourceLocationName: str, MaxResults: int = None, NextToken: str = None
    ) -> ListVodSourcesResponseTypeDef:
        """
        [Client.list_vod_sources documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.list_vod_sources)
        """

    def put_channel_policy(self, ChannelName: str, Policy: str) -> Dict[str, Any]:
        """
        [Client.put_channel_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.put_channel_policy)
        """

    def put_playback_configuration(
        self,
        AdDecisionServerUrl: str = None,
        AvailSuppression: "AvailSuppressionTypeDef" = None,
        Bumper: "BumperTypeDef" = None,
        CdnConfiguration: "CdnConfigurationTypeDef" = None,
        ConfigurationAliases: Dict[str, Dict[str, str]] = None,
        DashConfiguration: DashConfigurationForPutTypeDef = None,
        LivePreRollConfiguration: "LivePreRollConfigurationTypeDef" = None,
        ManifestProcessingRules: "ManifestProcessingRulesTypeDef" = None,
        Name: str = None,
        PersonalizationThresholdSeconds: int = None,
        SlateAdUrl: str = None,
        Tags: Dict[str, str] = None,
        TranscodeProfileName: str = None,
        VideoContentSourceUrl: str = None,
    ) -> PutPlaybackConfigurationResponseTypeDef:
        """
        [Client.put_playback_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.put_playback_configuration)
        """

    def start_channel(self, ChannelName: str) -> Dict[str, Any]:
        """
        [Client.start_channel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.start_channel)
        """

    def stop_channel(self, ChannelName: str) -> Dict[str, Any]:
        """
        [Client.stop_channel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.stop_channel)
        """

    def tag_resource(self, ResourceArn: str, Tags: Dict[str, str]) -> None:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.tag_resource)
        """

    def untag_resource(self, ResourceArn: str, TagKeys: List[str]) -> None:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.untag_resource)
        """

    def update_channel(
        self, ChannelName: str, Outputs: List[RequestOutputItemTypeDef]
    ) -> UpdateChannelResponseTypeDef:
        """
        [Client.update_channel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.update_channel)
        """

    def update_source_location(
        self,
        HttpConfiguration: "HttpConfigurationTypeDef",
        SourceLocationName: str,
        AccessConfiguration: "AccessConfigurationTypeDef" = None,
        DefaultSegmentDeliveryConfiguration: "DefaultSegmentDeliveryConfigurationTypeDef" = None,
    ) -> UpdateSourceLocationResponseTypeDef:
        """
        [Client.update_source_location documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.update_source_location)
        """

    def update_vod_source(
        self,
        HttpPackageConfigurations: List["HttpPackageConfigurationTypeDef"],
        SourceLocationName: str,
        VodSourceName: str,
    ) -> UpdateVodSourceResponseTypeDef:
        """
        [Client.update_vod_source documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Client.update_vod_source)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_channel_schedule"]
    ) -> GetChannelSchedulePaginator:
        """
        [Paginator.GetChannelSchedule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.GetChannelSchedule)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        [Paginator.ListChannels documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.ListChannels)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_playback_configurations"]
    ) -> ListPlaybackConfigurationsPaginator:
        """
        [Paginator.ListPlaybackConfigurations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.ListPlaybackConfigurations)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_source_locations"]
    ) -> ListSourceLocationsPaginator:
        """
        [Paginator.ListSourceLocations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.ListSourceLocations)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_vod_sources"]) -> ListVodSourcesPaginator:
        """
        [Paginator.ListVodSources documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.ListVodSources)
        """
