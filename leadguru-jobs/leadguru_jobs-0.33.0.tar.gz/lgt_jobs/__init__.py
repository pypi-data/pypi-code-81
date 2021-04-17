from .basejobs import (BaseBackgroundJobData, BaseBackgroundJob, InvalidJobTypeException)
from .bots_stats import BotStatsUpdateJob, BotsCredentialsUpdateJob, RestartBotsJob, LoadChatHistoryJob, \
    UserBotsCredentialsUpdateJob, UpdateUserSlackProfileJob
from .analytics import TrackAnalyticsJob
from .smtp import SendMailJob
from .leads import ArchiveLeadsJob
from .runner import (BackgroundJobRunner)
from .simple_job import (SimpleTestJob)

jobs_map = {
    "SimpleTestJob": SimpleTestJob,
    "BotStatsUpdateJob": BotStatsUpdateJob,
    "ArchiveLeadsJob": ArchiveLeadsJob,
    "BotsCredentialsUpdateJob": BotsCredentialsUpdateJob,
    "RestartBotsJob": RestartBotsJob,
    "SendMailJob": SendMailJob,
    "TrackAnalyticsJob": TrackAnalyticsJob,
    "LoadChatHistoryJob": LoadChatHistoryJob,
    "UserBotsCredentialsUpdateJob": UserBotsCredentialsUpdateJob,
    "UpdateUserSlackProfileJob": UpdateUserSlackProfileJob
}
__all__ = [
    # Jobs
    SimpleTestJob,
    BotStatsUpdateJob,
    ArchiveLeadsJob,
    BotsCredentialsUpdateJob,
    RestartBotsJob,
    SendMailJob,
    SimpleTestJob,
    LoadChatHistoryJob,
    UserBotsCredentialsUpdateJob,
    UpdateUserSlackProfileJob,

    # module classes
    BackgroundJobRunner,
    BaseBackgroundJobData,
    BaseBackgroundJob,
    InvalidJobTypeException,

    # mapping
    jobs_map
]
