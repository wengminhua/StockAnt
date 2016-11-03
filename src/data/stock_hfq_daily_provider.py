# coding:utf-8
import tushare as ts
from db_engine import get_db_engine
from pandas import read_sql_query
import datetime
from stock_basic_provider import StockBasicProvider
import pandas as pd


class StockHfqDailyProvider:
    def __init__(self):
        return

    @classmethod
    def get_data(cls, stock_code, start_date=None, end_date=None):
        cls.__fill_data(stock_code, end_date)
        if start_date is None:
            start_date = StockBasicProvider.get_first_trade_date(stock_code)
        if end_date is None:
            end_date = datetime.date.today()
        engine = get_db_engine()
        sql = "SELECT code,date,open,high,close,low,volume FROM t_daily_hfq WHERE code='%s' and date between '%s' and '%s' ORDER BY date" % (stock_code, cls.__date_to_str(start_date), cls.__date_to_str(end_date))
        df = read_sql_query(sql, engine)
        return df

    @classmethod
    def __fill_data(cls, stock_code, end_date=None):
        engine = get_db_engine()
        start_date = None
        sql = "SELECT * FROM t_daily_hfq WHERE code='%s' ORDER BY date DESC LIMIT 1" % stock_code
        df = read_sql_query(sql, engine)
        if df.size >= 1:
            if end_date is None:
                if df["date"][0].date() == datetime.date.today():
                    return
                start_date = df["date"][0].date() + datetime.timedelta(days=1)
                end_date = datetime.date.today()
            else:
                if df["date"][0].date() >= end_date:
                    return
                start_date = df["date"][0].date() + datetime.timedelta(days=1)
        else:
            start_date = StockBasicProvider.get_first_trade_date(stock_code)
            if end_date is None:
                end_date = datetime.date.today()
            if start_date > end_date:
                start_date = end_date

        while True:
            temp_end = start_date + datetime.timedelta(days=600)
            if temp_end >= end_date:
                temp_end = end_date
            while True:
                try:
                    df = ts.get_h_data(stock_code, start=cls.__date_to_str(start_date), end=cls.__date_to_str(temp_end), autype="hfq")
                    break
                except Exception as err:
                    print("Tushare exeption:" + err.message)
            if df is not None:
                df["code"] = pd.Series(stock_code, index=df.index)
                df.to_sql("t_daily_hfq", engine, if_exists="append")
            start_date = temp_end + datetime.timedelta(days=1)
            if start_date >= end_date:
                break

    @staticmethod
    def __date_to_str(date):
        return str(date)[0:10]
