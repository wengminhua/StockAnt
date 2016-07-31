import time
import datetime


def parseDate(date_str):
    date_time = time.strptime(date_str, '%Y-%m-%d')
    return datetime.date(date_time.tm_year, date_time.tm_mon, date_time.tm_mday)


def parseNumber(num_str):
    if not num_str.isdigit():
        return None
    if num_str.find(r'.') >= 0:
        return float(num_str)
    else:
        return int(num_str)


def parseBool(bool_str):
    if bool_str == 'True' or bool_str == 'true':
        return True
    elif bool_str == 'False' or bool_str == 'false':
        return False
    else:
        return None