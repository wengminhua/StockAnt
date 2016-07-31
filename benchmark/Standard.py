#coding:utf-8


def profit_and_loss(trade_df):
    pnl = 0
    for i in range(0, trade_df["date"].size):
        if cmp(trade_df["direction"][i], "buy") == 0:
            pnl -= trade_df["volume"][i] * trade_df["price"][i]
        elif cmp(trade_df["direction"][i], "sell") == 0:
            pnl += trade_df["volume"][i] * trade_df["price"][i]
    return pnl