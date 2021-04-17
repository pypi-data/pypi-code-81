import asyncio
import datetime
from pytz import timezone as tz
import re

import schoolInfo.util as util


@util.except_keyError
async def meal(
    ATPT_OFCDC_SC_CODE: str,
    SD_SCHUL_CODE: str,
    MLSV_YMD: datetime.datetime = None,
    timezone: str = "Asia/Seoul",
    auth_key: str = None,
) -> dict:
    MLSV_YMD = datetime.datetime.now(tz(timezone)) if MLSV_YMD is None else MLSV_YMD
    MLSV__YMD = re.sub("[^0-9]", "", str(MLSV_YMD.__str__()))[2:8]

    addition = [
        f"MLSV_YMD={MLSV__YMD}",
        f"ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}",
        f"SD_SCHUL_CODE={SD_SCHUL_CODE}",
    ]
    url: str = util.url_manager(
        type="mealServiceDietInfo", additions=addition, auth_key=auth_key
    ).url
    meal_data = (await util.HTMLGetter().get_json(url))["mealServiceDietInfo"][1]["row"]
    return meal_data
