import datetime
from requester.profession import NiceRequester
from requester.nirvana import NirvanaRequester
from utils.dateutils import datetime2str_z, str2datetime
from config import CLASS_CARD_HOST, CLASS_CARD_PORT, NICE_HOST, NICE_PROTOCOL
from utils.redis_utils import RedisCache
from utils.code import get_md5_hash
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


def upload_student_attendance(content):
    logger.info(">>> Process upload_student_attendance")
    attendance_id, school_id = content['attendance_id'], content['school_id']
    nirvana_requester = NirvanaRequester(school_id=school_id, host=CLASS_CARD_HOST, port=CLASS_CARD_PORT)
    attendance_data = nirvana_requester.get_student_attendance_info(attendance_id)
    record_time = attendance_data['record_time']
    if not record_time:
        return
    school_data = nirvana_requester.get_school_info(school_id)
    school_number = school_data['code'] or "1499"
    nice_requester = NiceRequester(school_number, protocol=NICE_PROTOCOL, host=NICE_HOST)
    record_time = str2datetime(record_time)
    checking_time = datetime2str_z(record_time - datetime.timedelta(hours=8))
    student_data = nirvana_requester.get_student_info(content['student_id'])
    classroom_num = attendance_data['classroom']['num']
    res = nice_requester.get_classroom_list()
    res_data = res.get('locations', [])
    location_id = None
    for rd in res_data:
        number = get_md5_hash(rd['locationName'])
        if number == classroom_num:
            location_id = rd['locationID']
            break
    if not location_id:
        logger.info("Can't find location_id {}".format(attendance_data))
        return
    attendance_data = {"checkingTime": checking_time, "studentEID": student_data['number'],
                       "locationID": location_id,
                       "cardID": student_data['ecard']['sn'] if student_data['ecard'] else None}
    redis_cache = RedisCache()
    redis_key = "student_attendance:{}".format(school_number)
    serial = int(redis_cache.get(redis_key)) or 0
    data = {"schoolID": school_number, "data": [attendance_data], "serial": serial}

    logger.info(">>> Nice RES upload_student_attendance:{}".format(data))
    nice_res = nice_requester.upload_attendance(data)
    logger.info(">>> Nice RES upload_student_attendance:{}, RES:{}".format(data, nice_res))
    redis_cache.set(redis_key, str(serial + 1))
