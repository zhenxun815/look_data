#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: file_utils.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/22/2019 9:28
import os
import re


def make_dirs(base_dir, sub_dir):
    _dir = os.path.join(base_dir, sub_dir)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    return _dir


def save_dict2file(dict2save: dict, dest_file: str, work=None, split=':'):
    print(f'start writing data to: {dest_file}')
    with open(dest_file, 'a', encoding='utf-8') as f:
        for k, v in dict2save.items():
            print(f'item to write k {k},v {v}')
            if work:
                k, v = work(k, v)
            f.write(f'{k}{split}{v}\n')
        f.flush()
    print(f'complete writing data to: {dest_file}')


def save_list2file(list2save, dest_file: str, work_func=None, filter_func=None, new_line=True):
    """
    write list elements to file line by line
    :param list2save:
    :param dest_file
    :param work_func: func, process each item in the list
    :param filter: func, filter item
    :return:
    """
    print(f'start writing data to: {dest_file}')
    with open(dest_file, 'a', encoding='utf-8') as f:
        for item in list2save:
            # print(f'item to write {item}')
            if not filter_func or filter_func(item):
                if work_func:
                    item = work_func(item)
                line = f'{str(item)}\n' if new_line else f' {str(item)}'
                f.write(line)
    print(f'complete writing data to: {dest_file}')


def get_files(dir_path, name_regx=None):
    """
    get files whose name match specified name patten under a dir, if file name
    patten is no specified, then return all files name
    :param dir_path:
    :param name_regx:
    :return:
    """
    if os.path.isdir(dir_path):
        files = os.listdir(dir_path)

        if name_regx:
            _pattern = re.compile(name_regx)
            return [os.path.join(dir_path, file) for file in files if _pattern.match(file)]
        return [os.path.join(dir_path, file) for file in files]
    else:
        raise Exception(f'{dir_path} is not a dir')


def read_line(file2read, work=None, split=None):
    print(f'start reading {file2read}')
    with open(file2read, encoding='utf-8') as f:
        for line in f:
            content = line.strip()
            if split:
                content = content.split(split)
            if work:
                # print(f'work content {content}')
                yield work(content)
            else:
                yield content
    print(f'complete reading {file2read}')


def remove_redundant(origin_file, dest_file, keep_order=True):
    """
    make lines unique and write to a new file
    :param keep_order: whether to keep the order of origin list or not
    :param origin_file:
    :param dest_file:
    :return:
    """
    print(f'origin file is: {origin_file}, dest file is: {dest_file}')
    lines = read_line(origin_file, lambda line: line)
    if keep_order:
        save_list2file(list(dict.fromkeys(lines)), dest_file)
    else:
        save_list2file(list(set(lines)), dest_file)


def join_file(new_file_path, old_file_path):
    for file2join in old_file_path:
        print(f'{file2join}')
        lines2write = read_line(file2join)
        save_list2file(lines2write, new_file_path)


if __name__ == '__main__':

    new_file = 'E:/ip_data/classification/201909/my_answers/my_answer09.txt'
    files = get_files('E:/ip_data/classification/201909/my_answers/')
    join_file(new_file, files)
