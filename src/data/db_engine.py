# coding:utf-8
from sqlalchemy import create_engine


def get_db_engine():
    return create_engine("mysql://root:123456@127.0.0.1/StockAnt?charset=utf8")
