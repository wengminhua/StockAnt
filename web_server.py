from flask import Flask,jsonify,request
from check_modules import load_modules
from check_modules import output_modules
from utils.stock_ant import StockAnt as ant
from backtest import backtest
from data.history_daily_provider import HistoryDailyProvider
import utils.parser
import subprocess
import os
from multiprocessing import Process
app = Flask(__name__, static_folder="D:/projects/Hackathon/StockAnt/workspace/webroot/static/")
g_user_modules = []


@app.route("/")
def index():
    return app.send_static_file("build.html")


@app.route("/<path:path>")
def web_root(path):
    return app.send_static_file(path)


@app.route("/api/methods", methods=["POST"])
def get_modules():
    all_modules = request.data
    if len(g_user_modules) > 0:
        all_modules = all_modules + ',' + ','.join(g_user_modules)
    p = subprocess.Popen("python check_modules.py " + all_modules + " ./webroot/static/job/methods.json",shell=True, cwd="D:/projects/Hackathon/StockAnt/workspace/")
    p.wait()
    #module_paths = request.data.split(",")
    #load_modules(module_paths)
    #methods = ant.get_methods()
    #return jsonify({"methods": methods})
    return app.send_static_file("job/methods.json")

@app.route("/api/run", methods=["POST"])
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


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files['file']
    f.save(os.path.join("D:/projects/Hackathon/StockAnt/workspace/user/", request.form['name']+".py"))
    g_user_modules.append('user.'+request.form['name'])
    return app.send_static_file("build.html")

if __name__ == "__main__":
    app.run()
