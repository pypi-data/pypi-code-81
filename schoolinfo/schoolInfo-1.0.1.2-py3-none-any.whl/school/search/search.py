import asyncio

from schoolInfo.util import url_manager, HTMLGetter, except_keyError


@except_keyError
async def search(keyword: str, auth_key: str = None) -> dict:
    url: str = url_manager(
        type="schoolInfo", additions=[f"SCHUL_NM={keyword}"], auth_key=auth_key
    ).get_url()
    return (await HTMLGetter().get_json(url))["schoolInfo"][1]["row"][0]
