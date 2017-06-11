# coding:utf-8


def profit_and_loss(trade_df, stock_df):
    pnl = 0
    for i in range(0, trade_df["date"].size):
        if cmp(trade_df["direction"][i], "buy") == 0:
            pnl -= trade_df["volume"][i] * trade_df["price"][i]
        elif cmp(trade_df["direction"][i], "sell") == 0:
            pnl += trade_df["volume"][i] * trade_df["price"][i]
    return pnl


def buy_and_sell_count(trade_df, stock_df):
    buy_count = 0
    sell_count = 0
    for i in range(0, trade_df["date"].size):
        if cmp(trade_df["direction"][i], "buy") == 0:
            buy_count += 1
        elif cmp(trade_df["direction"][i], "sell") == 0:
            sell_count += 1
    return [buy_count, sell_count]


def profit_and_loss_count(trade_df, stock_df):
    profit_count = 0
    loss_count = 0
    holding = 0
    cost_price = 0
    for i in range(0, trade_df["date"].size):
        if cmp(trade_df["direction"][i], "buy") == 0:
            balance = cost_price * holding + trade_df["volume"][i] * trade_df["price"][i]
            holding += trade_df["volume"][i]
            cost_price = balance / holding
        elif cmp(trade_df["direction"][i], "sell") == 0:
            if trade_df["price"][i] >= cost_price:
                profit_count += 1
            else:
                loss_count += 1
            holding -= trade_df["volume"][i]
    return [profit_count, loss_count]


def profit_and_loss_percentage(trade_df, stock_df):
    pnl_rate = 0
    holding = 0
    cost_price = 0
    for i in range(0, trade_df["date"].size):
        if cmp(trade_df["direction"][i], "buy") == 0:
            balance = cost_price * holding + trade_df["volume"][i] * trade_df["price"][i]
            holding += trade_df["volume"][i]
            cost_price = balance / holding
        elif cmp(trade_df["direction"][i], "sell") == 0:
            one_pnl_rate = (trade_df["price"][i] - cost_price) / cost_price
            pnl_rate += one_pnl_rate
            holding -= trade_df["volume"][i]
    return pnl_rate * 100


def reference_profit_and_loss_percentage(trade_df, stock_df):
    size = stock_df["date"].size
    if size <= 0:
        return 0
    buy_price = stock_df["open"][0]
    sell_price = stock_df["close"][size-1]
    return (sell_price - buy_price) / buy_price * 100
