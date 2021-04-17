import asyncio
import datetime
import re

from schoolInfo.util import url_manager, HTMLGetter, except_keyError


@except_keyError
async def schedule(
    ATPT_OFCDC_SC_CODE: str,
    SD_SCHUL_CODE: str,
    start_date: datetime.datetime = None,
    end_date: datetime.datetime = None,
    auth_key: str = None,
):
    try:
        start_date = re.sub("[^0-9]", "", str(start_date.__str__()))[2:8]
        end_date = re.sub("[^0-9]", "", str(end_date.__str__()))[2:8]
    except Exception as err:
        print(err)

    addition = [
        f"ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}",
        f"SD_SCHUL_CODE={SD_SCHUL_CODE}",
        f"AA_FROM_YMD={start_date}" f"AA_TO_YMD={end_date}",
    ]

    url: str = url_manager(
        type="SchoolSchedule", additions=addition, auth_key=auth_key
    ).get_url()
    return (await HTMLGetter().get_json(url))["SchoolSchedule"][1]["row"]
