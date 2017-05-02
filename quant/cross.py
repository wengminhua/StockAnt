# coding:utf-8
import pandas as pd
import utils.valid
from utils.stock_ant import StockAnt as ant


@ant.register(step="quant", types=["series", "series"])
def cross(a_series, b_series):
    output_arr = []
    for i in range(0, len(a_series)):
        if i == 0:
            output_arr.append(None)
            continue
        prev_a = a_series[i - 1]
        prev_b = b_series[i - 1]
        a = a_series[i]
        b = b_series[i]
        if not utils.valid.is_valid_numbers([prev_a, prev_b, a, b]):
            output_arr.append(None)
            continue
        if prev_a > prev_b and b > a:
            output_arr.append(-1)
        elif prev_a < prev_b and b < a:
            output_arr.append(1)
        else:
            output_arr.append(0)
    return pd.Series(output_arr)
