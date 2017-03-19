# coding:utf-8
import tushare as ts
import datetime


class StockBasicProvider:

    _basic_df = None
    _industry_df = None
    _hs300_df = None

    def __init__(self):
        return

    @classmethod
    def __get_basic_df(cls):
        if cls._basic_df is None:
            cls._basic_df = ts.get_stock_basics()
        return cls._basic_df

    @classmethod
    def __get_industry_df(cls):
        if cls._industry_df is None:
            cls._industry_df = ts.get_industry_classified()
        return cls._industry_df

    @classmethod
    def __get_hs300_df(cls):
        if cls._hs300_df is None:
            cls._hs300_df = ts.get_hs300s()
        return cls._hs300_df

    @classmethod
    def can_trade(cls, stock_code):
        first_trade_date = cls.get_first_trade_date(stock_code)
        if first_trade_date is None:
            return False
        return True

    @classmethod
    def get_first_trade_date(cls, stock_code):
        basic_df = cls.__get_basic_df()
        long_date = basic_df.ix[stock_code]["timeToMarket"]
        if long_date <= 0:
            return None
        year = long_date / 10000
        month = long_date % 10000 / 100
        day = long_date % 100
        return datetime.datetime(year, month, day).date()

    @classmethod
    def find_codes(cls, category, category_names = None):
        if category is None:
            return category_names
        stock_codes = []
        if cmp(category, "industry") == 0:
            df = cls.__get_industry_df()
            for i in range(0, df["c_name"].size):
                for category_name in category_names:
                    if cmp(df["c_name"][i], category_name) == 0:
                        stock_codes.append(df["code"][i])
        elif cmp(category, "hs300") == 0:
            df = cls.__get_hs300_df()
            for i in range(0, df["code"].size):
                stock_codes.append(df["code"][i])
        elif cmp(category, "all") == 0:
            df = cls.__get_basic_df()
            for i in range(0, len(df.index.values)):
                stock_codes.append(df.index.values[i])
        return stock_codes
