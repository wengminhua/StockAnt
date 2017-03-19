# coding:utf-8
import pandas as pd
import datetime


def trade(df, date_column, start_date, signal_column, buy_offset, buy_price_column, sell_offset, sell_price_column):
    trade_df = pd.DataFrame(columns=("date", "direction", "volume", "price"))
    holding = 0
    index = 0
    size = df[date_column].size - 1
    for i in range(0, size):
        date = df[date_column][i]
        if str(date)[0:10] < str(start_date):
            continue
        signal = df[signal_column][i]
        if signal is None:
            continue
        elif signal == 1:
            if holding == 0:
                trade_df.set_value(index, "date", df[date_column][i + buy_offset])
                trade_df.set_value(index, "direction", "buy")
                trade_df.set_value(index, "volume", 100)
                trade_df.set_value(index, "price", df[buy_price_column][i + buy_offset])
                holding += 100
                index += 1
        elif signal == -1:
            if holding > 0:
                trade_df.set_value(index, "date", df[date_column][i + sell_offset])
                trade_df.set_value(index, "direction", "sell")
                trade_df.set_value(index, "volume", 100)
                trade_df.set_value(index, "price", df[sell_price_column][i + sell_offset])
                holding -= 100
                index += 1
    if holding > 0:
        trade_df.set_value(index, "date", df[date_column][size - 1])
        trade_df.set_value(index, "direction", "sell")
        trade_df.set_value(index, "volume", holding)
        trade_df.set_value(index, "price", df[sell_price_column][size - 1])
        holding = 0

    return trade_df
