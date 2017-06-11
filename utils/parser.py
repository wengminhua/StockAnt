# coding:utf-8
import time
import datetime
import re


def parse_date(date_str):
    date_time = time.strptime(date_str, '%Y-%m-%d')
    return datetime.date(date_time.tm_year, date_time.tm_mon, date_time.tm_mday)


def parse_number(num_str):
    int_role = re.compile(r'^[-+]?[0-9]+$')
    float_role = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
    if float_role.match(num_str):
        return float(num_str)
    if int_role.match(num_str):
        return int(num_str)
    return None
    #if not num_str.isdigit():
    #    return None
    #if num_str.find(r'.') >= 0:
    #    return float(num_str)
    #else:
    #    return int(num_str)


def parse_bool(bool_str):
    if bool_str == 'True' or bool_str == 'true':
        return True
    elif bool_str == 'False' or bool_str == 'false':
        return False
    else:
        return None
