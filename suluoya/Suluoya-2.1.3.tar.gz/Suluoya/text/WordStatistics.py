import copy
import csv
import os
import PySimpleGUI as sg
from tqdm import tqdm
import jieba
from jieba import add_word
from jieba import lcut
import pdfplumber
from zhon.hanzi import punctuation
import string
import docx
import re
keywords = '''
数据
数字化
数据化
数字驱动
数据驱动
数据中心
数据应用
数据运用
数据挖掘
数据治理
大数据
数据治理委员会
首席数据官
数据仓库
数据集市
数据库
数据中台
数据平台
数据战略
数据管理
数据标准
信息安全
数据价值
数据质量
数据资产
可视化
数据分析
风险数据
数据管控数据模型
数据技术
数据支撑
数据支持
金融科技部
金融科技委员会
信息科技部
大数据部
数据管理和应用中心
'''
pun = string.punctuation+punctuation
n = True


def get_files(path):
    lists = []
    for filepath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            lists.append(filepath+'\\'+filename)
    return lists


def what(word):
    if word in pun:
        return '标点符号'
    elif word >= u'\u4e00' and word <= u'\u9fa5':
        return '中文'
    elif word.isdigit():
        return '数字'
    elif word.isalpha():
        return '英文'
    else:
        return '其他'


def sp(sentence):
    return [dict(zip(jieba.lcut(j), map(what, jieba.lcut(j)))) for j in sentence.split(' ') if j != '']


def calculate_pdf(file_name='bohaibank.pdf',
                  target={'数字化': 0, '数据化': 0, '数字驱动': 0},
                  what_dict={'标点符号': 0, '中文': 0, '数字': 0, '英文': 0, '其他': 0},
                  path=None, save_path=None):
    global n
    with pdfplumber.open(file_name) as pdf:
        pages = pdf.pages
        word_number = 0
        print('\n'+file_name)
        for page in tqdm(pages):
            try:
                index = page.extract_text().split('\n')[:-1]
                data = map(sp, index)
                for i in data:
                    for j in i:
                        for key, value in j.items():
                            word_number += len(key)
                            what_dict[value] += 1
                            if key in list(target.keys()):
                                target[key] += 1
            except:
                pass
    target['总字数'] = word_number
    target.update(what_dict)
    target['银行'] = file_name

    with open(f'{save_path}/result.csv', 'a+', newline='') as f:
        f_csv = csv.DictWriter(f, list(target.keys()))
        if n:
            f_csv.writeheader()
            n = False
        f_csv.writerow(target)
    # return target


def calculate_word(file_name='bohaibank.pdf',
                   target={'数字化': 0, '数据化': 0, '数字驱动': 0},
                   what_dict={'标点符号': 0, '中文': 0, '数字': 0, '英文': 0, '其他': 0},
                   path=None, save_path=None):
    global n
    file = docx.Document(file_name)
    index = []
    word_number = 0
    print('\n'+file_name)
    for para in tqdm(file.paragraphs):
        if para.text != None:
            index.append("".join(para.text.split()))
        data = map(sp, index)
        for i in data:
            for j in i:
                for key, value in j.items():
                    word_number += len(key)
                    what_dict[value] += 1
                    if key in list(target.keys()):
                        target[key] += 1
    target['总字数'] = word_number
    target.update(what_dict)
    target['银行'] = file_name
    with open(f'{save_path}/result.csv', 'a+', newline='') as f:
        f_csv = csv.DictWriter(f, list(target.keys()))
        if n:
            f_csv.writeheader()
            n = False
        f_csv.writerow(target)


def gui():
    global keywords
    keywords = keywords[1:]
    sg.theme('BlueMono')
    layout = [
        [sg.FolderBrowse('选择文件夹', key='path')],
        [sg.Text('关键词')],
        [sg.Multiline(default_text=keywords, key='keywords',)],
        [sg.Text('类型')],
        [sg.Checkbox(text='标点符号', default=True),
         sg.Checkbox(text='中文', default=True),
         sg.Checkbox(text='数字', default=True),
         sg.Checkbox(text='英文', default=True),
         sg.Checkbox(text='其他', default=True), ],
        [sg.FolderBrowse('保存路径', key='save_path')],
        [sg.Button('戳这里ヾ(≧▽≦*)o')],
    ]
    window = sg.Window('( •̀ ω •́ )✧', layout)
    event, values = window.read()
    if event == 'Cancel' or event is None:
        window.close()
    keywords = values['keywords'][:-1].split('\n')
    target = {}
    for key in keywords:
        target[key] = 0
    what_dict = {}
    if values[0]:
        what_dict['标点符号'] = 0
    if values[1]:
        what_dict['中文'] = 0
    if values[2]:
        what_dict['数字'] = 0
    if values[3]:
        what_dict['英文'] = 0
    if values[4]:
        what_dict['其他'] = 0
    path = values['path']
    save_path = values['save_path']
    window.close()
    return target, what_dict, path, save_path


def file_guess(filename):
    try:
        return re.findall(r'\.(.*)', filename)[0]
    except:
        print(filename+'error')
        return None


def file_statistics():
    target, what_dict, path, save_path = gui()
    target_z = copy.deepcopy(target)
    what_dict_z = copy.deepcopy(what_dict)
    while save_path == '':
        print('保存路径？？？？？？？？？？？？？？')
        target, what_dict, path, save_path = gui()
    while path == '':
        print('路径？？？？？？？？？？？？？？')
        target, what_dict, path, save_path = gui()
    for i in target:
        jieba.add_word(i)
    filenames = get_files(path)
    for filename in tqdm(filenames):
        f = file_guess(filename)
        if f == 'pdf' or f == 'PDF':
            try:
                calculate_pdf(file_name=filename,
                              target=target, what_dict=what_dict,
                              path=path, save_path=save_path)
            except:
                print(filename)
        elif f == 'docx' or f == 'doc':
            try:
                calculate_word(file_name=filename,
                               target=target, what_dict=what_dict,
                               path=path, save_path=save_path)
            except:
                print(filename)
        target = copy.deepcopy(target_z)
        what_dict = copy.deepcopy(what_dict_z)

    print('\n(*≧︶≦))(￣▽￣* )ゞ')


if __name__ == '__main__':
    file_statistics()
