# coding:utf-8
import pandas as pd
from utils.stock_ant import StockAnt as ant


@ant.register(step="trade", types=["series", "series", "series", "series", "series", "boolean", "number"])
def trade(date_series, buy_signal_series, buy_price_series, sell_signal_series, sell_price_series, ignore_both_signals,
          min_holding_days):
    trade_df = pd.DataFrame(columns=("date", "direction", "volume", "price"))
    holding = 0
    index = 0
    holding_days = 0
    size = date_series.size - 1
    for i in range(0, size):
        date = date_series[i]
        # if str(date)[0:10] < str(start_date):
        #    continue
        if holding > 0:
            holding_days += 1
        else:
            holding_days = 0
        if holding > 0 and holding_days <= min_holding_days:
            continue
        signal = 0
        if ignore_both_signals:
            if buy_signal_series[i] and sell_signal_series[i]:
                continue
            if buy_signal_series[i]:
                signal = 1
            if sell_signal_series[i]:
                signal = -1
        else:
            if buy_signal_series[i] and holding <= 0:
                signal = 1
            if sell_signal_series[i] and holding > 0:
                signal = -1
        if signal == 0:
            continue
        elif signal == 1:
            if holding == 0:
                trade_df.set_value(index, "date", date)
                trade_df.set_value(index, "direction", "buy")
                trade_df.set_value(index, "volume", 100)
                trade_df.set_value(index, "price", buy_price_series[i])
                holding += 100
                index += 1
        elif signal == -1:
            if holding > 0:
                trade_df.set_value(index, "date", date)
                trade_df.set_value(index, "direction", "sell")
                trade_df.set_value(index, "volume", 100)
                trade_df.set_value(index, "price", sell_price_series[i])
                holding -= 100
                index += 1
    if holding > 0:
        trade_df.set_value(index, "date", date_series[size-1])
        trade_df.set_value(index, "direction", "sell")
        trade_df.set_value(index, "volume", holding)
        trade_df.set_value(index, "price", sell_price_series[size-1])
        holding = 0
    return trade_df
