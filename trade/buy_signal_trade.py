# coding:utf-8
import pandas as pd
import datetime
from utils.stock_ant import StockAnt as ant


@ant.register(step="trade", types=["series", "series", "series", "series", "series", "series", "number", "number", "number", "number", "number", "number"])
def trade(date_series, buy_price_series, high_price_series, low_price_series, close_price_series, signal_series, signal_continue_limit, buy_signal_offset, profit_limit, loss_limit, profit_limit_step, loss_limit_step):
    trade_df = pd.DataFrame(columns=("date", "direction", "volume", "price"))
    holding_volume = 0
    holding_price = 0
    holding_days = 0
    max_holding_volume = 100
    row = 0
    signal_continue_count = 0
    for i in range(0, len(date_series)-buy_signal_offset):
        signal = signal_series[i]
        if holding_volume > 0:
            holding_days += 1
        if signal is None:
            signal_continue_count = 0
            continue
        if signal == 1:
            signal_continue_count += 1
            if signal_continue_count >= signal_continue_limit and holding_volume < max_holding_volume:
                date = date_series[i + buy_signal_offset]
                direction = "buy"
                volume = 100
                price = buy_price_series[i + buy_signal_offset]
                holding_price = (holding_volume * holding_price + volume * price) / (holding_volume + volume)
                holding_volume += volume
                trade_df.set_value(row, "date", date)
                trade_df.set_value(row, "direction", direction)
                trade_df.set_value(row, "volume", 100)
                trade_df.set_value(row, "price", price)
                row += 1
        else:
            signal_continue_count = 0
            if holding_volume > 0:
                high_price = high_price_series[i]
                low_price = low_price_series[i]
                # 先考虑止损，再考虑止盈。
                if ((holding_price - low_price) / holding_price) >= (loss_limit - loss_limit_step * holding_days):
                    date = date_series[i]
                    direction = "sell"
                    volume = holding_volume
                    # price = holding_price - holding_price * loss_limit
                    price = low_price
                    holding_volume = 0
                    holding_price = 0
                    holding_days = 0
                    trade_df.set_value(row, "date", date)
                    trade_df.set_value(row, "direction", direction)
                    trade_df.set_value(row, "volume", volume)
                    trade_df.set_value(row, "price", price)
                    row += 1
                    continue
                if ((high_price - holding_price) / holding_price) >= (profit_limit - profit_limit_step * holding_days):
                    date = date_series[i]
                    direction = "sell"
                    volume = holding_volume
                    # price = holding_price + holding_price * profit_limit
                    price = holding_price + holding_price * (profit_limit - profit_limit_step * holding_days)
                    holding_volume = 0
                    holding_price = 0
                    holding_days = 0
                    trade_df.set_value(row, "date", date)
                    trade_df.set_value(row, "direction", direction)
                    trade_df.set_value(row, "volume", volume)
                    trade_df.set_value(row, "price", price)
                    row += 1
                    continue
    last_index = len(date_series) - 1
    if holding_volume > 0:
        date = date_series[last_index]
        direction = "sell"
        volume = holding_volume
        price = close_price_series[last_index]
        holding_volume = 0
        holding_price = 0
        holding_days = 0
        trade_df.set_value(row, "date", date)
        trade_df.set_value(row, "direction", direction)
        trade_df.set_value(row, "volume", volume)
        trade_df.set_value(row, "price", price)
    return trade_df
