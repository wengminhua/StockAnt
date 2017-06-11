# coding:utf-8
import datetime
from db_engine import get_db_engine
from pandas import read_sql_table


class StockBasicProvider:

    _basic_df = None
    _industry_df = None
    _concept_df = None
    _area_df = None
    _sme_df = None
    _gem_df = None
    _st_df = None
    _hs300_df = None
    _sz50_df = None
    _zz500_df = None

    def __init__(self):
        return

    @classmethod
    def __get_basic_df(cls):
        if cls._basic_df is None:
            engine = get_db_engine()
            cls._basic_df = read_sql_table("t_stock_basics", engine, index_col='code')
        return cls._basic_df

    @classmethod
    def __get_industry_df(cls):
        if cls._industry_df is None:
            engine = get_db_engine()
            cls._industry_df = read_sql_table("t_industry_classified", engine)
        return cls._industry_df

    @classmethod
    def __get_concept_df(cls):
        if cls._concept_df is None:
            engine = get_db_engine()
            cls._concept_df = read_sql_table("t_concept_classified", engine)
        return cls._concept_df

    @classmethod
    def __get_area_df(cls):
        if cls._area_df is None:
            engine = get_db_engine()
            cls._area_df = read_sql_table("t_area_classified", engine)
        return cls._area_df

    @classmethod
    def __get_sme_df(cls):
        if cls._sme_df is None:
            engine = get_db_engine()
            cls._sme_df = read_sql_table("t_sme", engine)
        return cls._sme_df

    @classmethod
    def __get_gem_df(cls):
        if cls._gem_df is None:
            engine = get_db_engine()
            cls._gem_df = read_sql_table("t_gem", engine)
        return cls._gem_df

    @classmethod
    def __get_st_df(cls):
        if cls._st_df is None:
            engine = get_db_engine()
            cls._st_df = read_sql_table("t_st", engine)
        return cls._st_df

    @classmethod
    def __get_hs300_df(cls):
        if cls._hs300_df is None:
            engine = get_db_engine()
            cls._hs300_df = read_sql_table("t_hs300s", engine)
        return cls._hs300_df

    @classmethod
    def __get_sz50_df(cls):
        if cls._sz50_df is None:
            engine = get_db_engine()
            cls._sz50_df = read_sql_table("t_sz50s", engine)
        return cls._sz50_df

    @classmethod
    def __get_zz500_df(cls):
        if cls._zz500_df is None:
            engine = get_db_engine()
            cls._zz500_df = read_sql_table("t_zz500s", engine)
        return cls._zz500_df

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
    def find_codes(cls, category, category_names=None):
        if category is None:
            return category_names
        stock_codes = []
        if cmp(category, "industry") == 0:
            df = cls.__get_industry_df()
            for i in range(0, df["c_name"].size):
                for category_name in category_names:
                    if cmp(df["c_name"][i], category_name) == 0:
                        stock_codes.append(df["code"][i])
        elif cmp(category, "concept") == 0:
            df = cls.__get_concept_df()
            for i in range(0, df["c_name"].size):
                for category_name in category_names:
                    if cmp(df["c_name"][i], category_name) == 0:
                        stock_codes.append(df["code"][i])
        elif cmp(category, "area") == 0:
            df = cls.__get_area_df()
            for i in range(0, df["area"].size):
                for category_name in category_names:
                    if cmp(df["area"][i], category_name) == 0:
                        stock_codes.append(df["code"][i])
        elif cmp(category, "sme") == 0:
            df = cls.__get_sme_df()
            for i in range(0, df["code"].size):
                stock_codes.append(df["code"][i])
        elif cmp(category, "gem") == 0:
            df = cls.__get_gem_df()
            for i in range(0, df["code"].size):
                stock_codes.append(df["code"][i])
        elif cmp(category, "st") == 0:
            df = cls.__get_st_df()
            for i in range(0, df["code"].size):
                stock_codes.append(df["code"][i])
        elif cmp(category, "hs300") == 0:
            df = cls.__get_hs300_df()
            for i in range(0, df["code"].size):
                stock_codes.append(df["code"][i])
        elif cmp(category, "sz50") == 0:
            df = cls.__get_sz50_df()
            for i in range(0, df["code"].size):
                stock_codes.append(df["code"][i])
        elif cmp(category, "zz500") == 0:
            df = cls.__get_zz500_df()
            for i in range(0, df["code"].size):
                stock_codes.append(df["code"][i])
        elif cmp(category, "all") == 0:
            df = cls.__get_basic_df()
            for i in range(0, len(df.index.values)):
                stock_codes.append(df.index.values[i])
        return stock_codes
