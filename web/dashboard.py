from flask import Flask, jsonify, request
from backtest import backtest
from data.history_daily_provider import HistoryDailyProvider
import utils.parser
import pandas as pd
import os
import sys
import getopt


g_app = Flask(__name__, static_folder="./static/")
g_result_path = None


@g_app.route("/")
def index():
    return g_app.send_static_file("dashboard.html")


@g_app.route("/<path:path>")
def web_root(path):
    return g_app.send_static_file(path)


@g_app.route("/api/benchmark", methods=["GET"])
def get_benchmark():
    global g_result_path
    benchmark_filename = os.path.join(g_result_path, "benchmark.csv")
    benchmark_df = pd.read_csv(benchmark_filename)
    result_arr = []
    for index, row in benchmark_df.iterrows():
        code = str(int(row["code"])).zfill(6)
        pnl = int(row["pnl"])
        result_arr.append({"code": code, "pnl": pnl})
    return jsonify(result_arr)


@g_app.route("/api/trade/<code>", methods=["GET"])
def get_trade(code):
    global g_result_path
    trade_filename = os.path.join(g_result_path, "trade.csv")
    trade_df = pd.read_csv(trade_filename)
    stock_trade_df = trade_df[trade_df.code == int(code)]
    result_arr = []
    for index, row in stock_trade_df.iterrows():
        date = row["date"]
        direction = row["direction"]
        price = row["price"]
        volume = row["volume"]
        result_arr.append({"date": date, "direction": direction, "price": price, "volume": volume})
    return jsonify(result_arr)


def main(argv=None):
    global g_result_path
    if argv is None:
        argv = sys.argv
    options, args = getopt.getopt(argv[1:], "r:p:", ["result=", "port="])
    for name, value in options:
        if name in ("-r", "--result"):
            g_result_path = value
        if name in ("-p", "--port"):
            port = value
    g_app.run(port=port)


if __name__ == "__main__":
    # sys.exit(main())
    g_result_path = "C:/Users/wengm/Projects/StockAnt/test/result/20170325/bias"
    g_app.run()
