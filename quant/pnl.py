# coding:utf-8
import pandas as pd
import utils.valid
from utils.stock_ant import StockAnt as ant

@ant.register(step="quant", types=["series", "series", "number"])
def max_profit_rate(buy_series, sell_series, holding):
    output_arr = []
    for index in range(input_series.size):
        if index < holding:
            output_arr.append(None)
            continue
        buy_price = buy_series[index - holding]
        max_sell_price = buy_price
        for offset in range(1, holding + 1):
            if sell_series[index + offset] > max_sell_price:
                max_sell_price = sell_series[index + offset]
        max_profit_rate = (max_sell_price - buy_price) / buy_price
        output_arr.append(max_profit_rate)
    return pd.Series(output_arr)


@ant.register(step="quant", types=["series", "series", "number"])
def max_loss_rate(buy_series, sell_series, holding):
    output_arr = []
    for index in range(input_series.size):
        if index < holding:
            output_arr.append(None)
            continue
        buy_price = buy_series[index - holding]
        min_sell_price = buy_price
        for offset in range(1, holding + 1):
            if sell_series[index + offset] < min_sell_price:
                min_sell_price = sell_series[index + offset]
        max_loss_rate = (buy_price - min_sell_price) / buy_price
        output_arr.append(max_loss_rate)
    return pd.Series(output_arr)
