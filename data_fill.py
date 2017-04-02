import pandas as pd
import tushare as ts
from data.db_engine import get_db_engine


def init_stock_basics():
    engine = get_db_engine()
    df = ts.get_stock_basics()
    sql = "delete from t_stock_basics"
    conn = engine.connect()
    conn.execute(sql)
    df.to_sql("t_stock_basics", engine, if_exists="append", index=True)


def init_industry_classified():
    engine = get_db_engine()
    df = ts.get_industry_classified()
    sql = "delete from t_industry_classified"
    conn = engine.connect()
    conn.execute(sql)
    df.to_sql("t_industry_classified", engine, if_exists="append", index=False)


def init_hs300s():
    engine = get_db_engine()
    df = ts.get_hs300s()
    sql = "delete from t_hs300s"
    conn = engine.connect()
    conn.execute(sql)
    df.to_sql("t_hs300s", engine, if_exists="append", index=False)


def main():
    init_stock_basics()
    init_industry_classified()
    init_hs300s()


if __name__ == "__main__":
    main()
