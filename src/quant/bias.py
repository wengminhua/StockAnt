# coding:utf-8
import pandas as pd
import utils.valid
from utils.stock_ant import StockAnt as ant


@ant.register(step="quant", types=["series", "series"])
def bias(close_series, ma_series):
    output_arr = []
    for i in range(0, len(close_series)):
        close = close_series[i]
        ma = ma_series[i]
        if utils.valid.is_valid_numbers([close, ma]):
            output_arr.append(((close - ma) / ma) * 100)
        else:
            output_arr.append(None)
    return pd.Series(output_arr)
