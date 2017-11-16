# coding:utf-8
import tushare as ts
import pandas as pd
from data.db_engine import get_db_engine
import datetime


def init_stock_basics():
    print "Init stock basic"
    engine = get_db_engine()
    df = ts.get_stock_basics()
    sql = "delete from t_stock_basics"
    conn = engine.connect()
    conn.execute(sql)
    df.to_sql("t_stock_basics", engine, if_exists="append", index=True)


def init_industry_classified():
    print "Init industry"
    engine = get_db_engine()
    df = ts.get_industry_classified()
    sql = "delete from t_industry_classified"
    conn = engine.connect()
    conn.execute(sql)
    df.to_sql("t_industry_classified", engine, if_exists="append", index=False)


def init_concept_classified():
    print "Init concept"
    engine = get_db_engine()
    df = ts.get_concept_classified()
    sql = "delete from t_concept_classified"
    conn = engine.connect()
    conn.execute(sql)
    df.to_sql("t_concept_classified", engine, if_exists="append", index=False)


def init_area_classified():
    print "Init area"
    engine = get_db_engine()
    df = ts.get_area_classified()
    sql = "delete from t_area_classified"
    conn = engine.connect()
    conn.execute(sql)
    df.to_sql("t_area_classified", engine, if_exists="append", index=False)


def init_sme():
    print "Init SME"
    engine = get_db_engine()
    df = ts.get_sme_classified()
    sql = "delete from t_sme"
    conn = engine.connect()
    conn.execute(sql)
    df.to_sql("t_sme", engine, if_exists="append", index=False)


def init_gem():
    print "Init GEM"
    engine = get_db_engine()
    df = ts.get_gem_classified()
    sql = "delete from t_gem"
    conn = engine.connect()
    conn.execute(sql)
    df.to_sql("t_gem", engine, if_exists="append", index=False)


def init_st():
    print "Init ST"
    engine = get_db_engine()
    df = ts.get_gem_classified()
    sql = "delete from t_st"
    conn = engine.connect()
    conn.execute(sql)
    df.to_sql("t_st", engine, if_exists="append", index=False)


def init_hs300s():
    print "Init HS300"
    engine = get_db_engine()
    df = ts.get_hs300s()
    sql = "delete from t_hs300s"
    conn = engine.connect()
    conn.execute(sql)
    df.to_sql("t_hs300s", engine, if_exists="append", index=False)


def init_sz50s():
    print "Init SZ50"
    engine = get_db_engine()
    df = ts.get_sz50s()
    sql = "delete from t_sz50s"
    conn = engine.connect()
    conn.execute(sql)
    df.to_sql("t_sz50s", engine, if_exists="append", index=False)


def init_zz500s():
    print "Init ZZ500"
    engine = get_db_engine()
    df = ts.get_zz500s()
    sql = "delete from t_zz500s"
    conn = engine.connect()
    conn.execute(sql)
    df.to_sql("t_zz500s", engine, if_exists="append", index=False)


def init_index():
    print "Init Index"
    engine = get_db_engine()
    df = ts.get_index()
    sql = "delete from t_index_basics"
    conn = engine.connect()
    conn.execute(sql)
    time_to_market_arr = []
    for i in range(0, len(df['code'])):
        index_code = df['code'][i]
        start_date = datetime.date(year=1980, month=1, day=1)
        end_date = start_date + datetime.timedelta(days=365)
        while True:
            try:
                # print index_code + " try: " + __date_to_str(start_date) + "-" + __date_to_str(end_date)
                k_df = ts.get_k_data(code=index_code, ktype='D', autype=None, index=True,
                                     start=__date_to_str(start_date), end=__date_to_str(end_date))
                if len(k_df['date']) > 0:
                    # print index_code + "'s start date is " + k_df['date'][0]
                    year = int(k_df['date'][0][0:4])
                    month = int(k_df['date'][0][5:7])
                    day = int(k_df['date'][0][8:10])
                    time_to_market_arr.append(year*10000 + month*100 + day)
                    break
                else:
                    start_date = start_date + datetime.timedelta(days=365)
                    end_date = start_date + datetime.timedelta(days=365)
            except:
                start_date = start_date + datetime.timedelta(days=365)
                end_date = start_date + datetime.timedelta(days=365)
    time_to_market_series = pd.Series(time_to_market_arr)
    df.insert(loc=len(df.columns), column="timeToMarket", value=time_to_market_series)
    df.to_sql("t_index_basics", engine, if_exists="append", index=False)


def __date_to_str(date):
    return str(date)[0:10]


def main():
    init_index()
    init_stock_basics()
    init_industry_classified()
    init_concept_classified()
    init_area_classified()
    init_sme()
    init_gem()
    init_st()
    init_hs300s()
    init_sz50s()
    init_zz500s()


if __name__ == "__main__":
    main()
