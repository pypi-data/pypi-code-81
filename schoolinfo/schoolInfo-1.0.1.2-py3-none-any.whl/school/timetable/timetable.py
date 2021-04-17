import asyncio

import schoolInfo.util as util


@util.except_keyError
async def timetable(
    ATPT_OFCDC_SC_CODE: str,
    SD_SCHUL_CODE: str,
    SCHUL_KND_SC_NM: str,
    auth_key: str = None,
):
    school_type: dict = {
        "초등학교": "elsTimetable",
        "중학교": "misTimetable",
        "고등학교": "hisTimetable",
        "특수학교": "spsTimetable",
    }

    addition: list = [
        f"ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}",
        f"SD_SCHUL_CODE={SD_SCHUL_CODE}",
    ]

    url: str = util.url_manager(
        type=school_type[SCHUL_KND_SC_NM], additions=addition, auth_key=auth_key
    ).get_url()
    return (await util.HTMLGetter().get_json(url))[school_type[SCHUL_KND_SC_NM]][1][
        "row"
    ]
