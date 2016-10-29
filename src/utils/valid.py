# coding:utf-8
import math


def is_valid_number(val):
    if val is None:
        return False
    if math.isnan(val):
        return False
    return True


def is_valid_numbers(val_list):
    for val in val_list:
        if not is_valid_number(val):
            return False
    return True
