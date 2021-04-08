import requests

import bs4
from tqdm import tqdm


def schmidt_tools(url, verbose=True):
    r""" Scrape the Schmidt Futures forum learning web page for Education project ideas

    >>> import os
    >>> from qary.constants import DATA_DIR
    >>> url = os.path.join(DATA_DIR, 'corpora', 'web_pages', 'Competition Finalists – Futures Forum.html')
    >>> projects = schmidt_tools(url=url, verbose=False)
    >>> len(projects)
    40
    """
    # url = 'https://futuresforumonlearning.org/competition-finalists/'

    if url.lower().strip().startswith('http'):
        page = requests.get(url).text
    else:
        with open(url) as fin:
            page = fin.read()
    soup = bs4.BeautifulSoup(page, features='lxml')
    finalists = soup.find_all('div', {'class': 'accrod-finalists'})
    if not finalists:
        winners_tabs = soup.find_all('div', {'class': 'comptitation-winner'})
        winners = []
        for div in winners_tabs:
            if div:
                winners.extend(list(
                    div.find_all('div', {'class': 'cata-org'}) or
                    div.find_all('div', {'class': 'mdw'})))
                # ipdb.set_trace()

    if verbose:
        print('# Schmidt Futures Tools Competition Finalists')
        print()
        print('1. [Small](#catalyst-prize-finalists)')
        print('2. [Medium](mid-range-prize-finalists)')
        print('3. [Large](large-prize-finalists)')

    projects = []
    for category in finalists:
        group = category.find('div', {'class': 'wpsm_panel-group'})
        tier = category.find('h3')
        if verbose:
            print()
            print()
            print('## ' + tier.text.strip())
            print()
        panels = group.find_all('div', {'class': 'wpsm_panel'})
        for panel in tqdm(panels):
            heading = panel.find('div', {'class': 'wpsm_panel-heading'})
            title = heading.find('h4', {'class': 'wpsm_panel-title'})
            collapsed = panel.find('div', {'class': 'wpsm_panel-collapse'})
            body = collapsed.find('div', {'class': "wpsm_panel-body"})
            team = body.h4.text.strip()
            paragraphs = [p.text.strip() for p in body.find_all('p')]
            if verbose:
                print('### ' + title.text.strip())
                print()
                print('#### ' + team)
                print()
                for p in paragraphs:
                    print('  ' + p)
                    print()
            projects.append({
                'team': team[5:].strip() if team.lower().startswith('team:') else team,
                'summary': paragraphs,
                'title': title.text.strip(),
                'category': tier.text})

    return projects
