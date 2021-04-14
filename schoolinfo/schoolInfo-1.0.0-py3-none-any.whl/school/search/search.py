import asyncio

from schoolInfo.util import url_manager, HTMLGetter


async def search(keyword: str) -> dict:
    url: str = url_manager(
        type="schoolInfo", additions=[f"SCHUL_NM={keyword}"]
    ).get_url()
    return (await HTMLGetter().get_json(url))["schoolInfo"][1]["row"][0]
