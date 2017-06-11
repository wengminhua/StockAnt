# coding:utf-8
import tushare as ts
from db_engine import get_db_engine
from pandas import read_sql_query
import datetime
from index_basic_provider import IndexBasicProvider
import pandas as pd


class IndexDailyProvider:
    def __init__(self):
        return

    @classmethod
    def get_data(cls, code, start_date=None, end_date=None):
        cls.__fill_data(code, end_date)
        if start_date is None:
            start_date = IndexBasicProvider.get_first_trade_date(code)
        if end_date is None:
            end_date = datetime.date.today()
        engine = get_db_engine()
        sql = "SELECT code,date,open,high,close,low,volume FROM t_daily_index WHERE code='%s' and date between '%s' and '%s' ORDER BY date" % (code, cls.__date_to_str(start_date), cls.__date_to_str(end_date))
        df = read_sql_query(sql, engine)
        return df

    @classmethod
    def __fill_data(cls, code, end_date=None):
        engine = get_db_engine()
        start_date = None
        sql = "SELECT * FROM t_daily_index WHERE code='%s' ORDER BY date DESC LIMIT 1" % code
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
            start_date = IndexBasicProvider.get_first_trade_date(code)
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
                    # df = ts.get_h_data(stock_code, start=cls.__date_to_str(start_date), end=cls.__date_to_str(temp_end), autype="hfq")
                    df = ts.get_k_data(code=code, ktype='D', autype=None, index=True,
                                       start=cls.__date_to_str(start_date), end=cls.__date_to_str(temp_end))
                    break
                except Exception as err:
                    print("Tushare exeption:" + err.message)
                    df = None
                    break
            if df is not None:
                df["code"] = pd.Series(code, index=df.index)
                df.to_sql("t_daily_index", engine, if_exists="append", index=False)
            start_date = temp_end + datetime.timedelta(days=1)
            if start_date >= end_date:
                break

    @staticmethod
    def __date_to_str(date):
        return str(date)[0:10]
