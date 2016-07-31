import math


def isValidNumber(val):
    if val is None:
        return False
    if math.isnan(val):
        return False
    return True


def isValidNumbers(val_list):
    for val in val_list:
        if not isValidNumber(val):
            return False
    return True