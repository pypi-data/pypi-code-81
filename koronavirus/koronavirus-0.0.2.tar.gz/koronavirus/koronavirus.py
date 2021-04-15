import requests, aiohttp

turkce = {
    "updated": "son_güncelleme",
    "cases": "vaka",
    "todayCases": "bugünkü_vaka",
    "deaths": "ölüm",
    "todayDeaths": "bugünkü_ölüm",
    "recovered": "iyileşen",
    "todayRecovered": "bugünkü_iyileşen",
    "active": "aktif_vaka",
    "critical": "kritik",
    "casesPerOneMillion": "milyon_başı_vaka",
    "deathsPerOneMillion": "milyon_başı_ölüm",
    "tests": "test",
    "testsPerOneMillion": "milyon_başı_test",
    "population": "nüfus",
    "continent": "kıta",
}


def korona(ulke: str = "Turkey") -> dict:
    response = requests.get(
        f"https://disease.sh/v3/covid-19/countries/{ulke}?yesterday=0&twoDaysAgo=0"
    )
    if response.status_code != 200:
        raise KoronavirusVeriHatasi(
            "Bir hata oluştu. Ülke adı İngilizce olmayabilir veya bu ülke ile ilgili veriler bulunmuyor olabilir."
        )
    data = response.json()
    turkce_data = {}
    for key in data.keys():
        try:
            turkce_data[turkce[key]] = data[key]
        except KeyError:
            continue
    return turkce_data


async def async_korona(ulke: str = "Turkey") -> dict:
    async with aiohttp.ClientSession() as ses:
        response = await ses.get(
            f"https://disease.sh/v3/covid-19/countries/{ulke}?yesterday=0&twoDaysAgo=0"
        )
    if response.status != 200:
        raise KoronavirusVeriHatasi(
            "Bir hata oluştu. Ülke adı İngilizce olmayabilir veya bu ülke ile ilgili veriler bulunmuyor olabilir."
        )
    data = await response.json()
    turkce_data = {}
    for key in data.keys():
        try:
            turkce_data[turkce[key]] = data[key]
        except KeyError:
            continue
    return turkce_data


class KoronavirusVeriHatasi(BaseException):
    pass
