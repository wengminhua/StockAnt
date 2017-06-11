# coding:utf-8
import datetime
from db_engine import get_db_engine
from pandas import read_sql_table


class IndexBasicProvider:

    _basic_df = None

    def __init__(self):
        return

    @classmethod
    def __get_basic_df(cls):
        if cls._basic_df is None:
            engine = get_db_engine()
            cls._basic_df = read_sql_table("t_index_basics", engine, index_col='code')
        return cls._basic_df

    @classmethod
    def get_first_trade_date(cls, index_code):
        basic_df = cls.__get_basic_df()
        long_date = basic_df.ix[index_code]["timeToMarket"]
        if long_date <= 0:
            return None
        year = long_date / 10000
        month = long_date % 10000 / 100
        day = long_date % 100
        return datetime.datetime(year, month, day).date()

    @classmethod
    def can_trade(cls, index_code):
        return True

    @classmethod
    def find_codes(cls, category, category_names=None):
        if category is None:
            return category_names
        index_codes = []
        if cmp(category, "all") == 0:
            df = cls.__get_basic_df()
            for i in range(0, len(df.index.values)):
                index_codes.append(df.index.values[i])
        return index_codes
