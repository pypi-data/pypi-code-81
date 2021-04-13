"""
Main interface for mediatailor service type definitions.

Usage::

    ```python
    from mypy_boto3_mediatailor.type_defs import AccessConfigurationTypeDef

    data: AccessConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccessConfigurationTypeDef",
    "AdBreakTypeDef",
    "AdMarkerPassthroughTypeDef",
    "AvailSuppressionTypeDef",
    "BumperTypeDef",
    "CdnConfigurationTypeDef",
    "ChannelTypeDef",
    "DashConfigurationTypeDef",
    "DashPlaylistSettingsTypeDef",
    "DefaultSegmentDeliveryConfigurationTypeDef",
    "HlsConfigurationTypeDef",
    "HlsPlaylistSettingsTypeDef",
    "HttpConfigurationTypeDef",
    "HttpPackageConfigurationTypeDef",
    "LivePreRollConfigurationTypeDef",
    "ManifestProcessingRulesTypeDef",
    "PlaybackConfigurationTypeDef",
    "ResponseOutputItemTypeDef",
    "ScheduleEntryTypeDef",
    "SlateSourceTypeDef",
    "SourceLocationTypeDef",
    "SpliceInsertMessageTypeDef",
    "TransitionTypeDef",
    "VodSourceTypeDef",
    "CreateChannelResponseTypeDef",
    "CreateProgramResponseTypeDef",
    "CreateSourceLocationResponseTypeDef",
    "CreateVodSourceResponseTypeDef",
    "DashConfigurationForPutTypeDef",
    "DescribeChannelResponseTypeDef",
    "DescribeProgramResponseTypeDef",
    "DescribeSourceLocationResponseTypeDef",
    "DescribeVodSourceResponseTypeDef",
    "GetChannelPolicyResponseTypeDef",
    "GetChannelScheduleResponseTypeDef",
    "GetPlaybackConfigurationResponseTypeDef",
    "ListChannelsResponseTypeDef",
    "ListPlaybackConfigurationsResponseTypeDef",
    "ListSourceLocationsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListVodSourcesResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutPlaybackConfigurationResponseTypeDef",
    "RequestOutputItemTypeDef",
    "ScheduleConfigurationTypeDef",
    "UpdateChannelResponseTypeDef",
    "UpdateSourceLocationResponseTypeDef",
    "UpdateVodSourceResponseTypeDef",
)

AccessConfigurationTypeDef = TypedDict(
    "AccessConfigurationTypeDef", {"AccessType": Literal["S3_SIGV4"]}, total=False
)

AdBreakTypeDef = TypedDict(
    "AdBreakTypeDef",
    {
        "MessageType": Literal["SPLICE_INSERT"],
        "OffsetMillis": int,
        "Slate": "SlateSourceTypeDef",
        "SpliceInsertMessage": "SpliceInsertMessageTypeDef",
    },
    total=False,
)

AdMarkerPassthroughTypeDef = TypedDict("AdMarkerPassthroughTypeDef", {"Enabled": bool}, total=False)

AvailSuppressionTypeDef = TypedDict(
    "AvailSuppressionTypeDef",
    {"Mode": Literal["OFF", "BEHIND_LIVE_EDGE"], "Value": str},
    total=False,
)

BumperTypeDef = TypedDict("BumperTypeDef", {"EndUrl": str, "StartUrl": str}, total=False)

CdnConfigurationTypeDef = TypedDict(
    "CdnConfigurationTypeDef",
    {"AdSegmentUrlPrefix": str, "ContentSegmentUrlPrefix": str},
    total=False,
)

_RequiredChannelTypeDef = TypedDict(
    "_RequiredChannelTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelState": str,
        "Outputs": List["ResponseOutputItemTypeDef"],
        "PlaybackMode": str,
    },
)
_OptionalChannelTypeDef = TypedDict(
    "_OptionalChannelTypeDef",
    {"CreationTime": datetime, "LastModifiedTime": datetime, "Tags": Dict[str, str]},
    total=False,
)


class ChannelTypeDef(_RequiredChannelTypeDef, _OptionalChannelTypeDef):
    pass


DashConfigurationTypeDef = TypedDict(
    "DashConfigurationTypeDef",
    {
        "ManifestEndpointPrefix": str,
        "MpdLocation": str,
        "OriginManifestType": Literal["SINGLE_PERIOD", "MULTI_PERIOD"],
    },
    total=False,
)

DashPlaylistSettingsTypeDef = TypedDict(
    "DashPlaylistSettingsTypeDef",
    {
        "ManifestWindowSeconds": int,
        "MinBufferTimeSeconds": int,
        "MinUpdatePeriodSeconds": int,
        "SuggestedPresentationDelaySeconds": int,
    },
    total=False,
)

DefaultSegmentDeliveryConfigurationTypeDef = TypedDict(
    "DefaultSegmentDeliveryConfigurationTypeDef", {"BaseUrl": str}, total=False
)

HlsConfigurationTypeDef = TypedDict(
    "HlsConfigurationTypeDef", {"ManifestEndpointPrefix": str}, total=False
)

HlsPlaylistSettingsTypeDef = TypedDict(
    "HlsPlaylistSettingsTypeDef", {"ManifestWindowSeconds": int}, total=False
)

HttpConfigurationTypeDef = TypedDict("HttpConfigurationTypeDef", {"BaseUrl": str})

HttpPackageConfigurationTypeDef = TypedDict(
    "HttpPackageConfigurationTypeDef",
    {"Path": str, "SourceGroup": str, "Type": Literal["DASH", "HLS"]},
)

LivePreRollConfigurationTypeDef = TypedDict(
    "LivePreRollConfigurationTypeDef",
    {"AdDecisionServerUrl": str, "MaxDurationSeconds": int},
    total=False,
)

ManifestProcessingRulesTypeDef = TypedDict(
    "ManifestProcessingRulesTypeDef",
    {"AdMarkerPassthrough": "AdMarkerPassthroughTypeDef"},
    total=False,
)

PlaybackConfigurationTypeDef = TypedDict(
    "PlaybackConfigurationTypeDef",
    {
        "AdDecisionServerUrl": str,
        "AvailSuppression": "AvailSuppressionTypeDef",
        "Bumper": "BumperTypeDef",
        "CdnConfiguration": "CdnConfigurationTypeDef",
        "ConfigurationAliases": Dict[str, Dict[str, str]],
        "DashConfiguration": "DashConfigurationTypeDef",
        "HlsConfiguration": "HlsConfigurationTypeDef",
        "LivePreRollConfiguration": "LivePreRollConfigurationTypeDef",
        "ManifestProcessingRules": "ManifestProcessingRulesTypeDef",
        "Name": str,
        "PersonalizationThresholdSeconds": int,
        "PlaybackConfigurationArn": str,
        "PlaybackEndpointPrefix": str,
        "SessionInitializationEndpointPrefix": str,
        "SlateAdUrl": str,
        "Tags": Dict[str, str],
        "TranscodeProfileName": str,
        "VideoContentSourceUrl": str,
    },
    total=False,
)

_RequiredResponseOutputItemTypeDef = TypedDict(
    "_RequiredResponseOutputItemTypeDef",
    {"ManifestName": str, "PlaybackUrl": str, "SourceGroup": str},
)
_OptionalResponseOutputItemTypeDef = TypedDict(
    "_OptionalResponseOutputItemTypeDef",
    {
        "DashPlaylistSettings": "DashPlaylistSettingsTypeDef",
        "HlsPlaylistSettings": "HlsPlaylistSettingsTypeDef",
    },
    total=False,
)


class ResponseOutputItemTypeDef(
    _RequiredResponseOutputItemTypeDef, _OptionalResponseOutputItemTypeDef
):
    pass


_RequiredScheduleEntryTypeDef = TypedDict(
    "_RequiredScheduleEntryTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ProgramName": str,
        "SourceLocationName": str,
        "VodSourceName": str,
    },
)
_OptionalScheduleEntryTypeDef = TypedDict(
    "_OptionalScheduleEntryTypeDef",
    {"ApproximateDurationSeconds": int, "ApproximateStartTime": datetime},
    total=False,
)


class ScheduleEntryTypeDef(_RequiredScheduleEntryTypeDef, _OptionalScheduleEntryTypeDef):
    pass


SlateSourceTypeDef = TypedDict(
    "SlateSourceTypeDef", {"SourceLocationName": str, "VodSourceName": str}, total=False
)

_RequiredSourceLocationTypeDef = TypedDict(
    "_RequiredSourceLocationTypeDef",
    {"Arn": str, "HttpConfiguration": "HttpConfigurationTypeDef", "SourceLocationName": str},
)
_OptionalSourceLocationTypeDef = TypedDict(
    "_OptionalSourceLocationTypeDef",
    {
        "AccessConfiguration": "AccessConfigurationTypeDef",
        "CreationTime": datetime,
        "DefaultSegmentDeliveryConfiguration": "DefaultSegmentDeliveryConfigurationTypeDef",
        "LastModifiedTime": datetime,
        "Tags": Dict[str, str],
    },
    total=False,
)


class SourceLocationTypeDef(_RequiredSourceLocationTypeDef, _OptionalSourceLocationTypeDef):
    pass


SpliceInsertMessageTypeDef = TypedDict(
    "SpliceInsertMessageTypeDef",
    {"AvailNum": int, "AvailsExpected": int, "SpliceEventId": int, "UniqueProgramId": int},
    total=False,
)

_RequiredTransitionTypeDef = TypedDict(
    "_RequiredTransitionTypeDef",
    {"RelativePosition": Literal["BEFORE_PROGRAM", "AFTER_PROGRAM"], "Type": str},
)
_OptionalTransitionTypeDef = TypedDict(
    "_OptionalTransitionTypeDef", {"RelativeProgram": str}, total=False
)


class TransitionTypeDef(_RequiredTransitionTypeDef, _OptionalTransitionTypeDef):
    pass


_RequiredVodSourceTypeDef = TypedDict(
    "_RequiredVodSourceTypeDef",
    {
        "Arn": str,
        "HttpPackageConfigurations": List["HttpPackageConfigurationTypeDef"],
        "SourceLocationName": str,
        "VodSourceName": str,
    },
)
_OptionalVodSourceTypeDef = TypedDict(
    "_OptionalVodSourceTypeDef",
    {"CreationTime": datetime, "LastModifiedTime": datetime, "Tags": Dict[str, str]},
    total=False,
)


class VodSourceTypeDef(_RequiredVodSourceTypeDef, _OptionalVodSourceTypeDef):
    pass


CreateChannelResponseTypeDef = TypedDict(
    "CreateChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelState": Literal["RUNNING", "STOPPED"],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "Outputs": List["ResponseOutputItemTypeDef"],
        "PlaybackMode": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

CreateProgramResponseTypeDef = TypedDict(
    "CreateProgramResponseTypeDef",
    {
        "AdBreaks": List["AdBreakTypeDef"],
        "Arn": str,
        "ChannelName": str,
        "CreationTime": datetime,
        "ProgramName": str,
        "SourceLocationName": str,
        "VodSourceName": str,
    },
    total=False,
)

CreateSourceLocationResponseTypeDef = TypedDict(
    "CreateSourceLocationResponseTypeDef",
    {
        "AccessConfiguration": "AccessConfigurationTypeDef",
        "Arn": str,
        "CreationTime": datetime,
        "DefaultSegmentDeliveryConfiguration": "DefaultSegmentDeliveryConfigurationTypeDef",
        "HttpConfiguration": "HttpConfigurationTypeDef",
        "LastModifiedTime": datetime,
        "SourceLocationName": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

CreateVodSourceResponseTypeDef = TypedDict(
    "CreateVodSourceResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "HttpPackageConfigurations": List["HttpPackageConfigurationTypeDef"],
        "LastModifiedTime": datetime,
        "SourceLocationName": str,
        "Tags": Dict[str, str],
        "VodSourceName": str,
    },
    total=False,
)

DashConfigurationForPutTypeDef = TypedDict(
    "DashConfigurationForPutTypeDef",
    {"MpdLocation": str, "OriginManifestType": Literal["SINGLE_PERIOD", "MULTI_PERIOD"]},
    total=False,
)

DescribeChannelResponseTypeDef = TypedDict(
    "DescribeChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelState": Literal["RUNNING", "STOPPED"],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "Outputs": List["ResponseOutputItemTypeDef"],
        "PlaybackMode": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

DescribeProgramResponseTypeDef = TypedDict(
    "DescribeProgramResponseTypeDef",
    {
        "AdBreaks": List["AdBreakTypeDef"],
        "Arn": str,
        "ChannelName": str,
        "CreationTime": datetime,
        "ProgramName": str,
        "SourceLocationName": str,
        "VodSourceName": str,
    },
    total=False,
)

DescribeSourceLocationResponseTypeDef = TypedDict(
    "DescribeSourceLocationResponseTypeDef",
    {
        "AccessConfiguration": "AccessConfigurationTypeDef",
        "Arn": str,
        "CreationTime": datetime,
        "DefaultSegmentDeliveryConfiguration": "DefaultSegmentDeliveryConfigurationTypeDef",
        "HttpConfiguration": "HttpConfigurationTypeDef",
        "LastModifiedTime": datetime,
        "SourceLocationName": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

DescribeVodSourceResponseTypeDef = TypedDict(
    "DescribeVodSourceResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "HttpPackageConfigurations": List["HttpPackageConfigurationTypeDef"],
        "LastModifiedTime": datetime,
        "SourceLocationName": str,
        "Tags": Dict[str, str],
        "VodSourceName": str,
    },
    total=False,
)

GetChannelPolicyResponseTypeDef = TypedDict(
    "GetChannelPolicyResponseTypeDef", {"Policy": str}, total=False
)

GetChannelScheduleResponseTypeDef = TypedDict(
    "GetChannelScheduleResponseTypeDef",
    {"Items": List["ScheduleEntryTypeDef"], "NextToken": str},
    total=False,
)

GetPlaybackConfigurationResponseTypeDef = TypedDict(
    "GetPlaybackConfigurationResponseTypeDef",
    {
        "AdDecisionServerUrl": str,
        "AvailSuppression": "AvailSuppressionTypeDef",
        "Bumper": "BumperTypeDef",
        "CdnConfiguration": "CdnConfigurationTypeDef",
        "ConfigurationAliases": Dict[str, Dict[str, str]],
        "DashConfiguration": "DashConfigurationTypeDef",
        "HlsConfiguration": "HlsConfigurationTypeDef",
        "LivePreRollConfiguration": "LivePreRollConfigurationTypeDef",
        "ManifestProcessingRules": "ManifestProcessingRulesTypeDef",
        "Name": str,
        "PersonalizationThresholdSeconds": int,
        "PlaybackConfigurationArn": str,
        "PlaybackEndpointPrefix": str,
        "SessionInitializationEndpointPrefix": str,
        "SlateAdUrl": str,
        "Tags": Dict[str, str],
        "TranscodeProfileName": str,
        "VideoContentSourceUrl": str,
    },
    total=False,
)

ListChannelsResponseTypeDef = TypedDict(
    "ListChannelsResponseTypeDef", {"Items": List["ChannelTypeDef"], "NextToken": str}, total=False
)

ListPlaybackConfigurationsResponseTypeDef = TypedDict(
    "ListPlaybackConfigurationsResponseTypeDef",
    {"Items": List["PlaybackConfigurationTypeDef"], "NextToken": str},
    total=False,
)

ListSourceLocationsResponseTypeDef = TypedDict(
    "ListSourceLocationsResponseTypeDef",
    {"Items": List["SourceLocationTypeDef"], "NextToken": str},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)

ListVodSourcesResponseTypeDef = TypedDict(
    "ListVodSourcesResponseTypeDef",
    {"Items": List["VodSourceTypeDef"], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutPlaybackConfigurationResponseTypeDef = TypedDict(
    "PutPlaybackConfigurationResponseTypeDef",
    {
        "AdDecisionServerUrl": str,
        "AvailSuppression": "AvailSuppressionTypeDef",
        "Bumper": "BumperTypeDef",
        "CdnConfiguration": "CdnConfigurationTypeDef",
        "ConfigurationAliases": Dict[str, Dict[str, str]],
        "DashConfiguration": "DashConfigurationTypeDef",
        "HlsConfiguration": "HlsConfigurationTypeDef",
        "LivePreRollConfiguration": "LivePreRollConfigurationTypeDef",
        "ManifestProcessingRules": "ManifestProcessingRulesTypeDef",
        "Name": str,
        "PersonalizationThresholdSeconds": int,
        "PlaybackConfigurationArn": str,
        "PlaybackEndpointPrefix": str,
        "SessionInitializationEndpointPrefix": str,
        "SlateAdUrl": str,
        "Tags": Dict[str, str],
        "TranscodeProfileName": str,
        "VideoContentSourceUrl": str,
    },
    total=False,
)

_RequiredRequestOutputItemTypeDef = TypedDict(
    "_RequiredRequestOutputItemTypeDef", {"ManifestName": str, "SourceGroup": str}
)
_OptionalRequestOutputItemTypeDef = TypedDict(
    "_OptionalRequestOutputItemTypeDef",
    {
        "DashPlaylistSettings": "DashPlaylistSettingsTypeDef",
        "HlsPlaylistSettings": "HlsPlaylistSettingsTypeDef",
    },
    total=False,
)


class RequestOutputItemTypeDef(
    _RequiredRequestOutputItemTypeDef, _OptionalRequestOutputItemTypeDef
):
    pass


ScheduleConfigurationTypeDef = TypedDict(
    "ScheduleConfigurationTypeDef", {"Transition": "TransitionTypeDef"}
)

UpdateChannelResponseTypeDef = TypedDict(
    "UpdateChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelState": Literal["RUNNING", "STOPPED"],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "Outputs": List["ResponseOutputItemTypeDef"],
        "PlaybackMode": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

UpdateSourceLocationResponseTypeDef = TypedDict(
    "UpdateSourceLocationResponseTypeDef",
    {
        "AccessConfiguration": "AccessConfigurationTypeDef",
        "Arn": str,
        "CreationTime": datetime,
        "DefaultSegmentDeliveryConfiguration": "DefaultSegmentDeliveryConfigurationTypeDef",
        "HttpConfiguration": "HttpConfigurationTypeDef",
        "LastModifiedTime": datetime,
        "SourceLocationName": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

UpdateVodSourceResponseTypeDef = TypedDict(
    "UpdateVodSourceResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "HttpPackageConfigurations": List["HttpPackageConfigurationTypeDef"],
        "LastModifiedTime": datetime,
        "SourceLocationName": str,
        "Tags": Dict[str, str],
        "VodSourceName": str,
    },
    total=False,
)
