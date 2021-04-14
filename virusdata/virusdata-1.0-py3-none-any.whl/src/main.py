import requests
import datetime

url = 'https://disease.sh/v3/covid-19/all'


def get_covid_deatails():
    """Get all the covid details."""

    res = requests.get(url)
    updated_at = res.json()['updated']
    data = res.json()
    date = datetime.datetime.fromtimestamp(updated_at/1e3)
    print(f"Updated at: {date}")
    print(f"Totol Cases: {data['cases']}")
    print(f"Total Deaths: {data['deaths']}")
    print(f"Total Recovery: {data['recovered']}")
    print(f"Total Critical Cases: {data['critical']}")
    print(f"Today Cases: {data['todayCases']}")
    print(f"Today Deaths: {data['todayDeaths']}")
    print(f"Today Recovered: {data['todayRecovered']}")
    print(f"Active Cases: {data['active']}")
    print(f"Cases Per Million(CPM): {data['casesPerOneMillion']}")
    print(f"Deaths Per Million(DPM): {data['deathsPerOneMillion']}")
    print(f"Tests Done: {data['tests']}")
    print(f"Population: {data['population']}")
    print(f"Total Affected Countries: {data['affectedCountries']}")


def display_data():
    """Display the values."""

    get_covid_deatails()


if __name__ == '__main__':
    display_data()
