# coding:utf-8
import pandas as pd
import utils.valid
from utils.stock_ant import StockAnt as ant


@ant.register(step="quant", types=["series", "string"])
def trend_continue_count(input_series):
    output_arr = []
    continue_count = 0
    for i in range(0, len(input_series)):
        if i == 0:
            output_arr.append(None)
        else:
            prev_val = input_series[i-1]
            val = input_series[i]
            if utils.valid.is_valid_numbers([prev_val, val]):
                if val > prev_val:
                    if continue_count > 0:
                        continue_count += 1
                    else:
                        continue_count = 1
                elif val == prev_val:
                    continue_count = 0
                else:
                    if continue_count < 0:
                        continue_count -= 1
                    else:
                        continue_count = -1
                output_arr.append(continue_count)
            else:
                output_arr.append(None)
    return pd.Series(output_arr)
