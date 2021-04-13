"""
Main interface for mediatailor service client paginators.

Usage::

    ```python
    import boto3

    from mypy_boto3_mediatailor import MediaTailorClient
    from mypy_boto3_mediatailor.paginator import (
        GetChannelSchedulePaginator,
        ListChannelsPaginator,
        ListPlaybackConfigurationsPaginator,
        ListSourceLocationsPaginator,
        ListVodSourcesPaginator,
    )

    client: MediaTailorClient = boto3.client("mediatailor")

    get_channel_schedule_paginator: GetChannelSchedulePaginator = client.get_paginator("get_channel_schedule")
    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_playback_configurations_paginator: ListPlaybackConfigurationsPaginator = client.get_paginator("list_playback_configurations")
    list_source_locations_paginator: ListSourceLocationsPaginator = client.get_paginator("list_source_locations")
    list_vod_sources_paginator: ListVodSourcesPaginator = client.get_paginator("list_vod_sources")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from mypy_boto3_mediatailor.type_defs import (
    GetChannelScheduleResponseTypeDef,
    ListChannelsResponseTypeDef,
    ListPlaybackConfigurationsResponseTypeDef,
    ListSourceLocationsResponseTypeDef,
    ListVodSourcesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetChannelSchedulePaginator",
    "ListChannelsPaginator",
    "ListPlaybackConfigurationsPaginator",
    "ListSourceLocationsPaginator",
    "ListVodSourcesPaginator",
)


class GetChannelSchedulePaginator(Boto3Paginator):
    """
    [Paginator.GetChannelSchedule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.GetChannelSchedule)
    """

    def paginate(
        self,
        ChannelName: str,
        DurationMinutes: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[GetChannelScheduleResponseTypeDef]:
        """
        [GetChannelSchedule.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.GetChannelSchedule.paginate)
        """


class ListChannelsPaginator(Boto3Paginator):
    """
    [Paginator.ListChannels documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.ListChannels)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListChannelsResponseTypeDef]:
        """
        [ListChannels.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.ListChannels.paginate)
        """


class ListPlaybackConfigurationsPaginator(Boto3Paginator):
    """
    [Paginator.ListPlaybackConfigurations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.ListPlaybackConfigurations)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPlaybackConfigurationsResponseTypeDef]:
        """
        [ListPlaybackConfigurations.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.ListPlaybackConfigurations.paginate)
        """


class ListSourceLocationsPaginator(Boto3Paginator):
    """
    [Paginator.ListSourceLocations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.ListSourceLocations)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListSourceLocationsResponseTypeDef]:
        """
        [ListSourceLocations.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.ListSourceLocations.paginate)
        """


class ListVodSourcesPaginator(Boto3Paginator):
    """
    [Paginator.ListVodSources documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.ListVodSources)
    """

    def paginate(
        self, SourceLocationName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListVodSourcesResponseTypeDef]:
        """
        [ListVodSources.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/mediatailor.html#MediaTailor.Paginator.ListVodSources.paginate)
        """
