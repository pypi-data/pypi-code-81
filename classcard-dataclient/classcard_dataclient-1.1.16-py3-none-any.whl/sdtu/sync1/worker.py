import time
from sync1.album import AlbumSync
from sync1.board import NoticeSync
from sync1.course import CourseTableSync
from sync1.news import NewsSync
from sync1.video import VideoSync
from sync1.exam import ExamSync
from sync1.classroom import ClassroomSync
from sync1.avatar import AvatarSync
from sync1.clear import ClearSync
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


def start_table_sync():
    start_time = time.time()
    classroom_sync = ClassroomSync()
    classroom_sync.start()
    course_table_sync = CourseTableSync()
    course_table_sync.bks_classroom_map = classroom_sync.bks_classroom_map
    course_table_sync.yjs_classroom_map = classroom_sync.yjs_classroom_map
    course_table_sync.need_relate_student = False
    course_table_sync.start()
    logger.info("course table sync used: {}s".format(round(time.time() - start_time, 4)))
    start_exam_sync()
    clear_sync = ClearSync()
    clear_sync.current_classroom_num = classroom_sync.current_classroom_num
    clear_sync.start()



def start_avatar_sync():
    start_time = time.time()
    avatar_sync = AvatarSync()
    avatar_sync.start()
    logger.info("avatar sync used: {}s".format(round(time.time() - start_time, 4)))


def start_crawl():
    start_time = time.time()
    for sync_class in [AlbumSync, VideoSync, NoticeSync, NewsSync]:
        crawler = sync_class()
        crawler.start()
    logger.info("info crawl used: {}s".format(round(time.time() - start_time, 4)))


def start_exam_sync():
    start_time = time.time()
    exam_sync = ExamSync()
    exam_sync.start()
    logger.info("exam sync used: {}s".format(round(time.time() - start_time, 4)))
