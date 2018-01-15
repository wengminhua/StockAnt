# coding:utf-8
import pandas as pd
from utils.stock_ant import StockAnt as ant


@ant.register(step="quant", types=["series", "series", "series", "number", "number", "number"])
def kdj(close_series, high_series, low_series, rsv_period, k_period, d_period):
    k_arr = []
    d_arr = []
    j_arr = []
    for i in range(0, len(close_series)):
        if i < rsv_period - 1:
            k_arr.append(50)
            d_arr.append(50)
            j_arr.append(50)
            continue
        n_current = close_series[i]
        n_low = low_series[i]
        n_high = high_series[i]
        for offset in range(0, rsv_period):
            if low_series[i - offset] < n_low:
                n_low = low_series[i - offset]
            if high_series[i - offset] > n_high:
                n_high = high_series[i - offset]
        n_rsv = (n_current - n_low) / (n_high - n_low) * 100.0
        prev_k = k_arr[i - 1]
        n_k = (n_rsv + (k_period - 1) * prev_k) / k_period
        prev_d = d_arr[i - 1]
        n_d = (n_k + (d_period - 1) * prev_d) / d_period
        n_j = 3 * n_k - 2 * n_d
        k_arr.append(n_k)
        d_arr.append(n_d)
        j_arr.append(n_j)
    return [pd.Series(k_arr), pd.Series(d_arr), pd.Series(j_arr)]
