# coding:utf-8
import pandas as pd
import utils.valid
from utils.stock_ant import StockAnt as ant


@ant.register(step="quant", types=["series", "number"])
def ema(input_series, period):
    output_arr = []
    for index in range(input_series.size):
        value = input_series[index]
        if not utils.valid.is_valid_number(value):
            continue
        if index == 0:
            output_arr.append(value)
            continue
        prev_ema = output_arr[index - 1]
        ema = (value - prev_ema) * 2 / (period + 1) + prev_ema
        output_arr.append(ema)
    return pd.Series(output_arr)
