from flask import Flask, jsonify
import utils.parser
import pandas as pd
import os
import sys
import getopt
import json
import utils.valid

g_app = Flask(__name__, static_folder="./static/")
g_strategy_filename = None
g_result_path = None


@g_app.route("/")
def index():
    return g_app.send_static_file("dashboard.html")


@g_app.route("/<path:path>")
def web_root(path):
    return g_app.send_static_file(path)

@g_app.route("/api/benchmark/define", methods=["GET"])
def get_benchmark_data():
    global g_strategy_filename, g_result_path
    # Check benchmark data defines
    job_file = file(g_strategy_filename)
    job = json.load(job_file, 'utf-8')
    result_arr = []
    for benchmark_define in job['benchmark']:
        benchmark_names = benchmark_define["name"].split(',')
        for benchmark_name in benchmark_names:
            result_arr.append(benchmark_name)
    return jsonify(result_arr)


@g_app.route("/api/benchmark/data", methods=["GET"])
def get_benchmark():
    global g_strategy_filename, g_result_path
    # Check benchmark data defines
    job_file = file(g_strategy_filename)
    job = json.load(job_file, 'utf-8')
    benchmark_filename = os.path.join(g_result_path, "benchmark.csv")
    benchmark_df = pd.read_csv(benchmark_filename)
    result_arr = []
    for idx, row in benchmark_df.iterrows():
        obj = dict()
        obj["code"] = str(int(row["code"])).zfill(6)
        for benchmark_define in job['benchmark']:
            benchmark_names = benchmark_define["name"].split(',')
            for benchmark_name in benchmark_names:
                obj[benchmark_name] = int(row[benchmark_name])
        result_arr.append(obj)
    return jsonify(result_arr)


@g_app.route("/api/trade/<code>", methods=["GET"])
def get_trade(code):
    global g_result_path
    trade_filename = os.path.join(g_result_path, "trade.csv")
    trade_df = pd.read_csv(trade_filename)
    stock_trade_df = trade_df[trade_df.code == int(code)]
    result_arr = []
    for idx, row in stock_trade_df.iterrows():
        date = row["date"][0:10]
        direction = row["direction"]
        price = row["price"]
        volume = row["volume"]
        result_arr.append({"date": date, "direction": direction, "price": price, "volume": volume})
    return jsonify(result_arr)


@g_app.route("/api/chart/<code>", methods=["GET"])
def get_chart(code):
    global g_strategy_filename, g_result_path
    data_filename = os.path.join(g_result_path, code + ".csv")
    data_df = pd.read_csv(data_filename)
    result = {
        "categoryData": [],
        "kLineData": [],
        "volumeData": [],
        "tradeData": {
            "buyData": [],
            "sellData": []
        },
        "strategyChartList": []
    }
    # Prepare default chart: KLine, Volume
    for idx, row in data_df.iterrows():
        date = row["date"]
        open_price = row["open"]
        high_price = row["high"]
        close_price = row["close"]
        low_price = row["low"]
        volume = row["volume"]
        result["categoryData"].append(date)
        result["kLineData"].append([open_price, close_price, low_price, high_price])
        result["volumeData"].append(volume)
    # Prepare trade data
    trade_filename = os.path.join(g_result_path, "trade.csv")
    trade_df = pd.read_csv(trade_filename)
    stock_trade_df = trade_df[trade_df.code == int(code)]
    for idx, row in stock_trade_df.iterrows():
        date = row["date"][0:10]
        direction = row["direction"]
        price = row["price"]
        volume = abs(row["volume"])
        if direction == "buy":
            result["tradeData"]["buyData"].append([date, 0, volume, price])
        elif direction == "sell":
            result["tradeData"]["sellData"].append([date, 0, volume, price])
    # Append strategy chart list
    job_file = file(g_strategy_filename)
    job = json.load(job_file, 'utf-8')
    for series_define in job['series']:
        if "chart" in series_define:
            series_name = series_define["name"]
            strategy_chart = {
                "index": series_define["chart"]["index"],
                "name": series_define["chart"]["name"],
                "type": series_define["chart"]["type"],
                "data": [],
            }
            for idx, row in data_df.iterrows():
                row_value = row[series_name]
                if utils.valid.is_valid_number(row_value):
                    strategy_chart["data"].append(row_value)
                else:
                    strategy_chart["data"].append(None)
            result["strategyChartList"].append(strategy_chart)
    return jsonify(result)


def main(argv=None):
    global g_strategy_filename, g_result_path
    if argv is None:
        argv = sys.argv
    options, args = getopt.getopt(argv[1:], "s:r:p:", ["strategy=", "result=", "port="])
    for name, value in options:
        if name in ("-s", "--strategy"):
            g_strategy_filename = value
        if name in ("-r", "--result"):
            g_result_path = value
        if name in ("-p", "--port"):
            port = value
    g_app.run(port=port)


if __name__ == "__main__":
    # sys.exit(main())
    g_strategy_filename = "C:/Users/wengm/Projects/StockAnt/workspace/strategy/ema_cross_cut.json"
    g_result_path = "D:/working/StockAnt/output/ema_cross"
    g_app.run()
