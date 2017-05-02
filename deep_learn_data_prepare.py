# coding:utf-8
from data.stock_hfq_daily_provider import StockHfqDailyProvider
from data.stock_basic_provider import StockBasicProvider


def filter_data_by_pnl(stock_code, pnl_period, pnl_rate, start_date=None, end_date=None):
    df = StockHfqDailyProvider.get_data(stock_code, start_date, end_date)
    df.sort_values(by="date", ascending=False, inplace=True)
    close_series = df["close"]
    high_series = df["high"]
    hit_count = 0
    date_arr = []
    skip = False
    skip_count = 0
    for i in range(0, len(close_series)):
        if skip:
            skip_count += 1
            if skip_count >= pnl_period:
                skip = False
            else:
                continue
        if i >= (pnl_period - 1):
            max_high = 0
            for j in range(0, pnl_period):
                if high_series[i-j] > max_high:
                    max_high = high_series[i-j]
            begin_close = close_series[i-pnl_period+1]
            if ((max_high - begin_close) / begin_close) >= pnl_rate:
                hit_count += 1
                date_arr.append(df["date"][i-pnl_period+1])
                skip = True
                skip_count = 0
    return hit_count, date_arr


if __name__ == "__main__":
    result_count, result_date_arr = filter_data_by_pnl('600000', 5, 0.2)
    print result_date_arr
    print result_count
    #stock_arr = StockBasicProvider.find_codes("all")
    #total_count = 0
    #for i in range(0, len(stock_arr)):
    #    result_count, result_date_arr = filter_data_by_pnl(stock_arr[i], 5, 0.1)
    #
    #    total_count += result_count
    #    print total_count
