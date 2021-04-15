from requests import get, post
from bs4 import BeautifulSoup
from .errors import ImgFail
import argparse, sys, os, json, hashlib, re

def main():
    HUB_URL = 'https://www.policenews.act.gov.au/views/ajax'
    reqargs = {
        "view_name": "content_listing_blocks",
        "view_display_id": "block",
        "pager_element": "3"
    }
    USAGE_MSG = 'act_police_archiver -o [OUTPUT DIR] -p [MEDIA RELEASE URL]'
    parser = argparse.ArgumentParser(description='Archive ACT Policing Media Releases', usage=USAGE_MSG)
    parser.add_argument('-o', dest='output_dir', type=str, help='Output directory for downloaded content.')
    parser.add_argument('-p', '--post', dest='purl', type=str, help='URL of media release to download.')
    args = parser.parse_args()

    if(not args.output_dir):
        print('Output directory (-o) is required.')
        sys.exit(USAGE_MSG)
    elif(args.output_dir[-1] == '"' or args.output_dir[-1] == "'"):
        args.output_dir = f'{args.output_dir[:-1]}/'
    elif(args.output_dir[-1] != '/' or args.output_dir[-1] != '\\'):
        args.output_dir += '/'

    if(not os.path.isdir(args.output_dir)):
        try:
            os.mkdir(args.output_dir)
        except:
            sys.exit(f'Could not create directory "{args.output_dir}"')

    if(args.purl):
        scrape_release(args.purl, args.output_dir)
    else:
        scrape_all(HUB_URL, reqargs, args.output_dir)

def scrape_all(url, reqargs, output_dir):
    last = int(BeautifulSoup(get('https://www.policenews.act.gov.au/news/media-releases').text, 'lxml').find('li', {'class': 'pager-last last'}).find('a')['href'][-3:])
    for i in range(last + 1):
        reqargs['page'] = f'0,0,0,{i}'
        for release in BeautifulSoup(json.loads(post(url, data=reqargs).text)[2]['data'], 'lxml').find('div', {'class': 'view-content'}).find_all('div', {'class': 'views-row'}):
            scrape_release(f"https://www.policenews.act.gov.au{release.find('h3').find('a')['href']}", output_dir)

def scrape_release(url, output_dir):
    article_data = BeautifulSoup(get(url).text, 'lxml').find('div', {'id': 'content'})
    _article_title = article_data.find('h1', {'id': 'page-title'}).text.strip()
    _time = article_data.find('span', {'property': 'dc:date dc:created'})['content'][:-6].replace(':', '').replace('T', '').replace('-', '')
    RELEASE_DIR = f"{output_dir}{_time} - {_article_title.replace(':', '_').replace('/', '-').replace('?', '_').replace('UPDATE ', '')} [{hashlib.md5(article_data.text.encode('utf-8')).hexdigest()[:6]}]/"
    IMG_DIR = f'{RELEASE_DIR}images/'

    if(not os.path.isdir(RELEASE_DIR)):
        print(f'Saving "{_article_title}"...')
        os.mkdir(RELEASE_DIR)
        _html = re.compile('[^\u0020-\u024F]').sub('', article_data.prettify().replace('\u25b2', '^').replace('\u2011', '-')) # Remove Chinese characters

        img_list = []
        for index,image in enumerate(article_data.find_all('img')):
            _file_key = [image['src'], f'{"{:02d}".format(index + 1)}.jpg']
            if(not _file_key[0] in img_list):
                img_list.append(_file_key[0])
                download_img(_file_key[0], _file_key[1], RELEASE_DIR)
                _html = _html.replace(_file_key[0], _file_key[1])

        for index,image in enumerate(article_data.find_all('a', {'class': 'colorbox'})):
            if(not os.path.isdir(IMG_DIR)):
                os.mkdir(IMG_DIR)
            _file_key = [image['href'], f'{"{:02d}".format(index + 1)}.jpg']
            if(not _file_key[0] in img_list):
                img_list.append(_file_key[0])
                download_img(_file_key[0], _file_key[1], IMG_DIR)
                _html = _html.replace(_file_key[0], f'images/{_file_key[1]}')

        with open(f'{RELEASE_DIR}index.html', 'w') as f:
            f.write(_html)
    else:
        print(f'Skipping "{_article_title}"...')
        

def download_img(url, title, output_dir):
    with open(output_dir + title, 'wb') as f:
        try:
            f.write(get(url).content)
            print(f'Downloading {url}...')
        except:
            pass