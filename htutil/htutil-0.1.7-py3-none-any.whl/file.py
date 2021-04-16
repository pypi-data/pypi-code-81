'''
Author: HaoTian Qi
Date: 2020-12-19 15:12:53
Description: file IO warpper
LastEditTime: 2021-04-16 21:57:56
LastEditors: HaoTian Qi
FilePath: \htutil\htutil\file.py
'''

import os
import pickle as pkl
import json


def read_all_text(path: str) -> str:
    with open(path, 'r', encoding='utf-8')as f:
        lines = f.readlines()
        text = ''.join(lines)
        return text


def read_all_lines(path: str) -> str:
    with open(path, 'r', encoding='utf-8')as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].replace('\n', '')
            lines[i] = lines[i].replace('\r', '')
        return lines


def write_all_text(path: str, content: str) -> None:
    content = str(content)
    create_dir_if_not_exist(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8')as f:
        f.write(content)


def write_all_lines(path: str, content: list) -> None:
    if not isinstance(content, list):
        raise TypeError('content is not list')
    create_dir_if_not_exist(os.path.dirname(path))
    text = '\n'.join(content)
    with open(path, 'w', encoding='utf-8')as f:
        f.write(text)


def append_all_text(path: str, content: str) -> None:
    content = str(content)
    with open(path, 'a', encoding='utf-8')as f:
        f.write(content)


def append_all_lines(path: str, content: list) -> None:
    if not isinstance(content, list):
        raise TypeError('content is not list')
    with open(path, 'a', encoding='utf-8')as f:
        text = '\n'.join(content)
        f.write(text)


def create_dir_if_not_exist(path: str) -> None:
    if path == '':
        return
    if not os.path.exists(path):
        os.makedirs(path)


def read_csv(path: str) -> None:
    lines = read_all_lines(path)
    rows = []
    for line in lines:
        rows.append(line.split(','))
    return rows


def write_csv(path: str, rows: list) -> None:
    lines = []
    for row in rows:
        for i in range(len(row)):
            row[i] = str(row[i])
        line = ','.join(row)
        lines.append(line)
    write_all_lines(path, lines)


def write_pkl(path: str, content) -> None:
    create_dir_if_not_exist(os.path.dirname(path))
    with open(path, 'wb') as f:
        pkl.dump(content, f)


def read_pkl(path: str):
    with open(path, 'rb') as f:
        result = pkl.load(f)
    return result


def write_json(path: str, content, indent=4) -> None:
    write_all_text(path, json.dumps(content, indent=indent))


def read_json(path: str):
    return json.loads(read_all_text(path))


def main():
    s = 'hello'
    write_all_text('1.txt', s)
    # hello in 1.txt
    append_all_text('1.txt', 'world')
    # helloworld in 1.txt
    s = read_all_text('1.txt')
    print(s)  # helloworld

    s = ['hello', 'world']
    write_all_lines('1.txt', s)
    # hello\nworld in 1.txt
    append_all_lines('1.txt', ['\npython'])
    # hello\nworld\npython in 1.txt
    s = read_all_lines('1.txt')
    print(s)  # ['hello', 'world', 'python']

    os.remove('1.txt')


if __name__ == '__main__':
    main()
