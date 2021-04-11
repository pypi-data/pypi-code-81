import csv
import json
import os

from bs4 import BeautifulSoup
import requests
from terminaltables import AsciiTable

FOLDER_TO_SAVE_RESULTS = "data/"


def parse_bing_one_page(keyword: str, page_number: int):
    """Extract URLs from one page of results of bing search.

    :param keyword: keyword to search
    :param page_number: bing results page number
    :return: list of URLs
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) "
                      "Gecko/20100101 Firefox/83.0"
    }
    params = {
        "q": keyword,
        "form": "QBLH",
        "first": page_number * 10,
    }
    url = "https://www.bing.com/search"

    response = requests.get(url, headers=headers, params=params, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "lxml")
    link_elements = soup.select("ol#b_results li.b_algo h2 a")
    return [
        (link_element.get("href"), link_element.text)
        for link_element in link_elements
    ]


def fetch_bing_search_results(keyword: str, results_number: int):
    """Extract results_number URLs from results of bing search.

    :param keyword: keyword to search
    :param results_number: number of results to extract
    :return: list of URLs
    """

    if results_number < 1 or not keyword:
        return None

    search_results = list()

    page_number = 0
    while len(search_results) < results_number:
        search_results += parse_bing_one_page(keyword, page_number)
        page_number += 1

    return search_results[:results_number]


def parse_duckduckgo(keyword: str, results_number: int):
    """Extract results_number of URLs from duckduckgo search.

    :param keyword: keyword to search
    :param results_number: number of UTLs to extract
    :return: list of URLs
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) "
                      "Gecko/20100101 Firefox/83.0"
    }
    params = {
        "q": keyword,
        "s": 0,
    }
    url = "https://duckduckgo.com/html/"

    response = requests.get(url, headers=headers, params=params, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "lxml")
    link_elements = soup.select("#links .links_main a")
    urls = [
        (href, link_element.text.strip())
        for link_element in link_elements
        if (href := link_element.get("href", ""))
    ]
    return urls[:results_number]


def fetch_urls_from_page(url: str):
    """Extract all urls from given page.

    :param url: given page to extract url
    :return: list of urls
    """

    response = requests.get(url)
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.content, "lxml")

    return [(url, a_elm.text.strip()) for a_elm in soup.select("a")
            if (url := a_elm.get("href", "")).startswith("https://")]


def fetch_urls_from_list_of_pages(urls: list, results_number: int):
    """Extract results_number urls from given pages.

    :param urls: given pages to extract urls
    :param results_number: number or urls to extract
    :return: list of urls
    """

    all_urls = []
    for url in urls:
        all_urls += fetch_urls_from_page(url[0])[:results_number]

    return all_urls


def save_urls_to_csv(urls: list, urls_second_rang=None):
    """Save a list of urls to csv file.

    :param urls: list of urls
    :param urls_second_rang: list of urls of 2nd rang if given
    :return: None
    """

    if urls_second_rang:
        urls += urls_second_rang

    with open(
            f"{FOLDER_TO_SAVE_RESULTS}urls.csv",
            mode="w",
            encoding="utf-8",
            newline="",
    ) as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(["URL link", "URL title"])
        writer.writerows(urls)


def save_urls_to_json(urls: list, urls_second_rang=None):
    """Save a list of urls to json file.

    :param urls: list of urls
    :param urls_second_rang: list of urls of 2nd rang if given
    :return: None
    """

    urls = {
        "urls_1st_rang": urls
    }
    if urls_second_rang:
        urls.update({
            "urls_2nd_rang": urls_second_rang,
        })

    with open(
            f"{FOLDER_TO_SAVE_RESULTS}urls.json",
            mode="w",
            encoding="utf-8"
    ) as file:
        json.dump(urls, file, ensure_ascii=False)


def print_to_console(urls: list, urls_second_rang=None):
    """Print a list of urls to the console.

    :param urls: list of urls
    :param urls_second_rang: list of urls of 2nd rang if given
    :return: None
    """

    table_data = [["URL link", "URL title"]]

    if urls_second_rang:
        urls += urls_second_rang

    for url in urls:
        table_data.append((url[0][:100], url[1][:100]))

    table = AsciiTable(table_data)
    print(table.table)


def search(
        engine="bing", format="json", keyword="python",
        number=3, number2=2, recursively=False,
):
    """Function that takes user input and performs operations accordingly.

    :param engine: search engine to use
    :param format: format to save results to
    :param keyword: keyword to search
    :param number: number of 1st rang urls to extract
    :param number2: number of 2nd rang urls to extract
    :param recursively: flag designating need to search 2nd rang urls
    :return: None
    """

    if engine == "duckduckgo" or engine == "duck":
        urls = parse_duckduckgo(keyword, number)
    else:
        urls = fetch_bing_search_results(keyword, number)

    if recursively:
        urls_second_rang = fetch_urls_from_list_of_pages(urls, number2)
    else:
        urls_second_rang = None

    os.makedirs(FOLDER_TO_SAVE_RESULTS, exist_ok=True)

    if format == "console":
        print_to_console(urls, urls_second_rang=urls_second_rang)
    elif format == "csv":
        save_urls_to_csv(urls, urls_second_rang=urls_second_rang)
    else:
        save_urls_to_json(urls, urls_second_rang)
