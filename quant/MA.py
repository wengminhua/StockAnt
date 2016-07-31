#coding:utf-8

import pandas as pd
import utils.Valid


def ma(input_series, period):
    output_arr = []
    temp_arr = []
    sum = 0
    for index in range(input_series.size):
        value = input_series[index]
        if not utils.Valid.isValidNumber(value):
            continue
        sum += value
        temp_arr.append(value)
        if len(temp_arr) == period:
            output_arr.append(sum / period)
            sum -= temp_arr[0]
            temp_arr.pop(0)
        else:
            output_arr.append(None)
    return pd.Series(output_arr)
