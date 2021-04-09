"""
Main interface for mediatailor service.

Usage::

    ```python
    import boto3
    from mypy_boto3_mediatailor import (
        Client,
        GetChannelSchedulePaginator,
        ListChannelsPaginator,
        ListPlaybackConfigurationsPaginator,
        ListSourceLocationsPaginator,
        ListVodSourcesPaginator,
        MediaTailorClient,
    )

    session = boto3.Session()

    client: MediaTailorClient = boto3.client("mediatailor")
    session_client: MediaTailorClient = session.client("mediatailor")

    get_channel_schedule_paginator: GetChannelSchedulePaginator = client.get_paginator("get_channel_schedule")
    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_playback_configurations_paginator: ListPlaybackConfigurationsPaginator = client.get_paginator("list_playback_configurations")
    list_source_locations_paginator: ListSourceLocationsPaginator = client.get_paginator("list_source_locations")
    list_vod_sources_paginator: ListVodSourcesPaginator = client.get_paginator("list_vod_sources")
    ```
"""
from mypy_boto3_mediatailor.client import MediaTailorClient
from mypy_boto3_mediatailor.paginator import (
    GetChannelSchedulePaginator,
    ListChannelsPaginator,
    ListPlaybackConfigurationsPaginator,
    ListSourceLocationsPaginator,
    ListVodSourcesPaginator,
)

Client = MediaTailorClient


__all__ = (
    "Client",
    "GetChannelSchedulePaginator",
    "ListChannelsPaginator",
    "ListPlaybackConfigurationsPaginator",
    "ListSourceLocationsPaginator",
    "ListVodSourcesPaginator",
    "MediaTailorClient",
)
