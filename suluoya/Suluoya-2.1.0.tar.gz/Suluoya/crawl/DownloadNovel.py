import os
import time

import parsel
import PySimpleGUI as sg
import requests
from termcolor import colored


def get_selector(url):
    resp = requests.get(url)
    resp.encoding = resp.apparent_encoding
    return parsel.Selector(resp.text)

# 获取书名


def get_book_url(searchkey='斗罗大陆'):
    data = {'searchkey': searchkey}
    resp = requests.post(
        'http://www.xbiquge.la/modules/article/waps.php', data=data)
    resp.encoding = resp.apparent_encoding
    selector = parsel.Selector(resp.text)
    trs = selector.css('.grid tr')
    book_info = {}
    for tr in trs[1:]:
        tds = tr.css('td')
        book_href = tds[0].css('a::attr(href)').getall()[0]
        book_name = tds[0].css('a::text').getall()[0]
        book_info[book_name] = book_href
    return book_info  # 包含书名和网址的字典

# 获取章节


def get_book_category(book_href):
    selector = get_selector(book_href)
    dds = selector.css('#list dd')
    book_category = {}
    for dd in dds:
        href = dd.css('a::attr(href)').getall()[0]
        chapter = dd.css('a::text').getall()[0]
        book_category[chapter] = 'http://www.paoshuzw.com'+href
    return book_category

# 获取章节具体内容


def get_book_content(chapter_url):
    selector = get_selector(chapter_url)
    contents = selector.css('#content::text').getall()
    return contents


# 线程锁，防止资源拥挤
#lock = threading.Lock()

# 保存函数


def save(book, charpter, contents, path):
    #global lock
    print(colored(f'Saving {book}--{charpter} ...', 'cyan'))
    # time.sleep(0.1)
    for i in contents:
        # lock.acquire()
        try:
            with open(f'{path}/{book}/{charpter}.txt', 'a', encoding='utf8') as f:
                f.write(i)
        except:
            print(f'\033[0;30;40m{i} erro!!!')
        # lock.release()

# 主函数


def main(info):
    charpter_url = info['charpter_url']
    book_name = info['book_name']
    charpter = info['charpter']
    path = info['path']
    contents = get_book_content(charpter_url)
    save(book_name, charpter, contents, path)

# 用户体验


def user(name):
    book_info = get_book_url(name)
    if book_info == {}:
        print(colored('输入的书名无效！', 'yellow'))
        # download_novel(name,path)
        raise ValueError('输入的书名无效！')
    num = 1
    print('-'*50)
    dict = {}
    for book_name, book_href in book_info.items():
        print(colored(f'{num} {book_name} {book_href}', 'green'))
        dict[str(num)] = (book_name, book_href)
        num += 1
    while 1:
        number = input('请输入序号：')
        try:
            book = dict[number]
            return book
        except KeyError:
            print(colored('Please input a existed number!', 'yellow'))


def download_novel(name, path):
    book = user(name)
    book_name = book[0]
    book_href = book[1]
    try:
        os.mkdir(path+'/'+book_name)
    except:
        pass
    book_category = get_book_category(book_href)
    for charpter, charpter_url in book_category.items():
        info = {}
        info['charpter_url'] = charpter_url
        info['book_name'] = book_name
        info['charpter'] = charpter
        info['path'] = path
        main(info)


def NovelDownloadGui():
    sg.theme('BlueMono')

    layout = [[sg.Text('Book Name',)],
              [sg.Input('斗破苍穹', key='book_name')],
              [sg.Button('Download', key='download')],
              [sg.FolderBrowse('choose a folder to save data', key='path')],
              ]

    window = sg.Window('Suluoya Novel Download', layout)

    event, values = window.read()
    name = values['book_name']
    path = values['path']
    if path == '':
        print(colored('Please choose a folder to save novels!', 'magenta'))
        window.close()
        NovelDownloadGui()
    if event == sg.WIN_CLOSED:
        window.close()
    elif event == 'download':
        print(colored('save at '+path, 'blue'))
        window.close()
        download_novel(name, path)


if __name__ == '__main__':
    NovelDownloadGui()
