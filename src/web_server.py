from flask import Flask,jsonify,request
from check_modules import load_modules
from utils.stock_ant import StockAnt as ant
from backtest import backtest
from data.history_daily_provider import HistoryDailyProvider
import utils.parser
app = Flask(__name__, static_folder="D:/working/StockAnt/webroot/static/")

@app.route("/")
def index():
    return app.send_static_file("build.html")


@app.route("/js/<path:path>")
def js(path):
    return app.send_static_file("js/"+path)


@app.route("/job/<path:path>")
def job(path):
    return app.send_static_file("job/"+path)


@app.route("/")

@app.route("/api/methods")
def get_modules():
    load_modules(['quant.bias', 'quant.combine', 'quant.compare', 'quant.find', 'quant.ma'])
    methods = ant.get_methods()
    return jsonify({"methods": methods})


@app.route("/api/add", methods=["POST"])
def add():
    job_filename = app.static_folder + "job/job.json"
    file = open(job_filename, "w")
    file.write(request.data)
    file.close()
    backtest(job_filename, app.static_folder+"job/")
    return jsonify({"trade_url": "/job/trade.csv", "benchmark_url": "/job/benchmark.csv"})


@app.route("/api/data", methods=["GET"])
def data():
    data_filename = app.static_folder + "/data/data.csv"
    code = request.args["code"]
    start_date = utils.parser.parse_date(request.args["start"])
    end_date = utils.parser.parse_date(request.args["end"])
    data_df = HistoryDailyProvider.get_data(code, start_date, end_date)
    data_df.to_csv(data_filename, index=False)
    return app.send_static_file("data/data.csv")


if __name__ == "__main__":
    app.run()
