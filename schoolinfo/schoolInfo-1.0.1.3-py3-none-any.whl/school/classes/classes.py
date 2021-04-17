import asyncio

import schoolInfo.util as util


@util.except_keyError
async def classes(ATPT_OFCDC_SC_CODE: str, SD_SCHUL_CODE: str, auth_key: str = None):

    addition: list = [
        f"ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}",
        f"SD_SCHUL_CODE={SD_SCHUL_CODE}",
    ]

    url: str = util.url_manager(
        type="classInfo", additions=addition, auth_key=auth_key
    ).get_url()
    return (await util.HTMLGetter().get_json(url))["classInfo"][1]["row"]
