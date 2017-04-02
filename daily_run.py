import os
import time
import backtest
import pandas as pd


def get_job_name(job_filename):
    job_file_basename = os.path.basename(job_filename)
    return job_file_basename[:-1*'.json'.__len__()]


def get_time_key():
    return time.strftime('%Y%m%d%H%M', time.localtime(time.time()))


def get_date_key():
    return time.strftime('%Y%m%d', time.localtime(time.time()))


def get_date_str(date_key):
    time_val = time.strptime(date_key, '%Y%m%d')
    return time.strftime('%Y-%m-%d 00:00:00', time_val)


def make_job_result_dir(job_filename, result_dir):
    job_name = get_job_name(job_filename)
    job_result_dir = os.path.join(result_dir, get_date_key(), job_name)
    if not os.path.exists(job_result_dir):
        os.makedirs(job_result_dir)
    return job_result_dir


def get_job_files(job_dir):
    job_files = []
    all_files = os.listdir(job_dir)
    for f in all_files:
        if os.path.isdir(f):
            continue
        if f.endswith('.json'):
            job_files.append(os.path.join(job_dir, f))
    return job_files


def analysis_job_result(job_name, job_result_dir):
    item_arr = []
    value_arr = []
    benchmark_df = pd.read_csv(os.path.join(job_result_dir, "benchmark.csv"))
    trade_df = pd.read_csv(os.path.join(job_result_dir, "trade.csv"))
    # Calculate PnL Summarize
    pnl_sum = benchmark_df['pnl'].sum()
    item_arr.append('pnl_sum')
    value_arr.append(pnl_sum)
    # Calculate Profit Count
    profit_count = len(benchmark_df[benchmark_df['pnl'] > 0].index)
    item_arr.append('profit_count')
    value_arr.append(profit_count)
    # Calculate Loss Count
    loss_count = len(benchmark_df[benchmark_df['pnl'] < 0].index)
    item_arr.append('loss_count')
    value_arr.append(loss_count)
    # Calculate PnL count
    pnl_count = profit_count - loss_count
    item_arr.append('pnl_count')
    value_arr.append(pnl_count)
    # Find Trade Signal
    today_key = get_date_key()
    buy_signal_df = trade_df[(trade_df['direction'] == 'buy') & (trade_df['date'] == get_date_str('20151014'))]
    code_arr = buy_signal_df['code'].values
    item_arr.extend(code_arr)
    value_arr.extend([1] * len(code_arr))
    return pd.DataFrame({
        'item': item_arr,
        job_name: value_arr
    })


def main():
    job_dir = 'C:/Users/wengm/Projects/StockAnt/test/job'
    result_dir = 'C:/Users/wengm/Projects/StockAnt/test/result'
    while True:
        current_time = get_time_key()
        current_date = get_date_key()
        print current_time
        if not current_time.endswith('17:00'):
            job_files = get_job_files(job_dir)
            analysis_df = None
            for job_file in job_files:
                job_name = get_job_name(job_file)
                job_result_dir = make_job_result_dir(job_file, result_dir)
                print(job_result_dir)
                backtest.backtest(job_file, job_result_dir)
                job_analysis_df = analysis_job_result(job_name, job_result_dir)
                if analysis_df is None:
                    analysis_df = job_analysis_df
                else:
                    analysis_df = pd.merge(analysis_df, job_analysis_df, how='outer', on='item')
                print(analysis_df)
            analysis_df = analysis_df.fillna(0)
            analysis_df.to_csv(os.path.join(result_dir, current_date + '.csv'), index=False)
            break
        else:
            time.sleep(60)


if __name__ == "__main__":
    main()
