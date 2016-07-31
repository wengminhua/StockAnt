#coding:utf-8
from sqlalchemy import create_engine
from pandas import read_sql_query
import pandas as pd
import tushare as ts
import datetime


G_STOCK_BASICS_DF = None


def get_db_engine():
    return create_engine("mysql://root:123456@127.0.0.1/StockAnt?charset=utf8")

def get_daily_hist_data(code, start=None, end=None):
    fill_daily_hist_data(code, end)
    if start is None:
        start = get_first_trade_date(code)
    if end is None:
        end = datetime.date.today()
    engine = get_db_engine()
    sql = "SELECT code,date,open,high,close,low,volume FROM t_daily_hist WHERE code='%s' and date between '%s' and '%s' ORDER BY date" % (code, date_to_str(start), date_to_str(end))
    df = read_sql_query(sql, engine)
    return df


def fill_daily_hist_data(code, end=None):
    engine = get_db_engine()
    start = None
    sql = "SELECT * FROM t_daily_hist WHERE code='%s' ORDER BY date DESC LIMIT 1" % code
    df = read_sql_query(sql, engine)
    if df.size >= 1:
        if end is None:
            if df["date"][0].date() == datetime.date.today():
                return
            start = df["date"][0].date() + datetime.timedelta(days=1)
            end = datetime.date.today()
        else:
            if df["date"][0].date() >= end:
                return
            start = df["date"][0].date() + datetime.timedelta(days=1)
    else:
        # get_hist_data只有3年内数据，所以从2014年统一开始
        start = datetime.date(2014, 1, 1)
        if end is None:
            end = datetime.date.today()

    while True:
        temp_end = start + datetime.timedelta(days=600)
        if temp_end >= end:
            temp_end = end
        while True:
            try:
                df = ts.get_hist_data(code, start=date_to_str(start), end=date_to_str(temp_end))
                break
            except Exception as err:
                print("Tushare exeption:" + err.message)
        if df is None:
            break
        df["code"] = pd.Series(code, index=df.index)
        df.to_sql("t_daily_hist", engine, if_exists="append")
        start = temp_end + datetime.timedelta(days=1)
        if start >= end:
            break


def get_daily_hfq_data(code, start=None, end=None):
    fill_daily_hfq_data(code, end)
    if start is None:
        start = get_first_trade_date(code)
    if end is None:
        end = datetime.date.today()
    engine = get_db_engine()
    sql = "SELECT code,date,open,high,close,low,volume FROM t_daily_hfq WHERE code='%s' and date between '%s' and '%s' ORDER BY date" % (code, date_to_str(start), date_to_str(end))
    df = read_sql_query(sql, engine)
    return df


def fill_daily_hfq_data(code, end=None):
    engine = get_db_engine()
    start = None
    sql = "SELECT * FROM t_daily_hfq WHERE code='%s' ORDER BY date DESC LIMIT 1" % code
    df = read_sql_query(sql, engine)
    if df.size >= 1:
        if end is None:
            if df["date"][0].date() == datetime.date.today():
                return
            start = df["date"][0].date() + datetime.timedelta(days=1)
            end = datetime.date.today()
        else:
            if df["date"][0].date() >= end:
                return
            start = df["date"][0].date() + datetime.timedelta(days=1)
    else:
        start = get_first_trade_date(code)
        if end is None:
            end = datetime.date.today()

    while True:
        temp_end = start + datetime.timedelta(days=600)
        if temp_end >= end:
            temp_end = end
        while True:
            try:
                df = ts.get_h_data(code, start=date_to_str(start), end=date_to_str(temp_end), autype="hfq")
                break
            except Exception as err:
                print("Tushare exeption:" + err.message)
        if df is not None:
            df["code"] = pd.Series(code, index=df.index)
            df.to_sql("t_daily_hfq", engine, if_exists="append")
        start = temp_end + datetime.timedelta(days=1)
        if start >= end:
            break


def is_tradable(code):
    global G_STOCK_BASICS_DF
    if G_STOCK_BASICS_DF is None:
        G_STOCK_BASICS_DF = ts.get_stock_basics()
    long_date = G_STOCK_BASICS_DF.ix[code]["timeToMarket"]
    if long_date <= 0:
        return False
    return True


def get_first_trade_date(code):
    global G_STOCK_BASICS_DF
    if G_STOCK_BASICS_DF is None:
        G_STOCK_BASICS_DF = ts.get_stock_basics()
    long_date = G_STOCK_BASICS_DF.ix[code]["timeToMarket"]
    year = long_date / 10000
    month = long_date % 10000 / 100
    day = long_date % 100
    return datetime.datetime(year, month, day).date()


def find_stocks(category, category_names = None):
    if category is None:
        return category_names
    stock_codes = []
    if cmp(category, "industry") == 0:
        df = ts.get_industry_classified()
        for i in range(0, df["c_name"].size):
            for category_name in category_names:
                if cmp(df["c_name"][i], category_name) == 0:
                    stock_codes.append(df["code"][i])
    elif cmp(category, "hs300") == 0:
        df = ts.get_hs300s()
        for i in range(0, df["code"].size):
            stock_codes.append(df["code"][i])
    elif cmp(category, "all") == 0:
        df = ts.get_stock_basics()
        for i in range(0, len(df.index.values)):
            stock_codes.append(df.index.values[i])
    return stock_codes

def date_to_str(date):
    return str(date)[0:10]
