import requests
from bs4 import BeautifulSoup


def get_links(site):
    html = requests.get(site).text
    soup = BeautifulSoup(html, 'html.parser').find_all('a')
    links = [link.get('href') for link in soup]
    return links

def is_downloadable(url):
    """
    check if the url contains a downloadable resource
    """
    if (url.find('pdf')!=-1) or (url.find('epub')!=-1) or (url.find('mobi')!=-1):
        print(url)
        return True
    else:
        return False

def downloadbook_from(site_url):
    all_links = get_links(site_url)
    for link in all_links:
        if(is_downloadable(link)):
            r=requests.get(link, allow_redirects = True)
            if link.find('/'):
                filename=link.rsplit('/', 1)[1]
                open(filename, 'wb').write(r.content)
