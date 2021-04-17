import asyncio
import datetime
from pytz import timezone as tz
import re

import schoolInfo.util as util


@util.except_keyError
async def major(
    ATPT_OFCDC_SC_CODE: str, SD_SCHUL_CODE: str = None, auth_key: str = None
):

    addition = [f"ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}"]

    if SD_SCHUL_CODE is not None:
        addition.append(f"SD_SCHUL_CODE={SD_SCHUL_CODE}")

    url: str = util.url_manager(
        type="schoolMajorinfo", additions=addition, auth_key=auth_key
    ).get_url()
    return (await util.HTMLGetter().get_json(url))["schoolMajorinfo"][1]["row"]
