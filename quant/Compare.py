import pandas as pd
import utils.Valid


def greater_than(a_series, b_series, a_factor=1, b_factor=1):
    output_arr = []
    for i in range(0, len(a_series)):
        a = a_series[i]
        b = b_series[i]
        if not utils.Valid.isValidNumbers([a, b]):
            output_arr.append(None)
            continue
        if a * a_factor > b * b_factor:
            output_arr.append(True)
        else:
            output_arr.append(False)
    return pd.Series(output_arr)


def greater_equal(a_series, b_series, a_factor=1, b_factor=1):
    output_arr = []
    for i in range(0, len(a_series)):
        a = a_series[i]
        b = b_series[i]
        if not utils.Valid.isValidNumbers([a, b]):
            output_arr.append(None)
            continue
        if a * a_factor >= b * b_factor:
            output_arr.append(True)
        else:
            output_arr.append(False)
    return pd.Series(output_arr)


def smaller_than(a_series, b_series, a_factor=1, b_factor=1):
    return greater_than(b_series, a_series, b_factor, a_factor)


def smaller_equal(a_series, b_series, a_factor=1, b_factor=1):
    return greater_equal(b_series, a_series, b_factor, a_factor)


def equal(a_series, b_series, a_factor=1, b_factor=1):
    output_arr = []
    for i in range(0, len(a_series)):
        a = a_series[i]
        b = b_series[i]
        if not utils.Valid.isValidNumbers([a, b]):
            output_arr.append(None)
            continue
        if a * a_factor == b * b_factor:
            output_arr.append(True)
        else:
            output_arr.append(False)
    return pd.Series(output_arr)


def not_equal(a_series, b_series, a_factor=1, b_factor=1):
    output_arr = []
    for i in range(0, len(a_series)):
        a = a_series[i]
        b = b_series[i]
        if not utils.Valid.isValidNumbers([a, b]):
            output_arr.append(None)
            continue
        if a * a_factor == b * b_factor:
            output_arr.append(False)
        else:
            output_arr.append(True)
    return pd.Series(output_arr)
