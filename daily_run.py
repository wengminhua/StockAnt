import os
import time
import backtest


def get_job_name(job_filename):
    job_file_basename = os.path.basename(job_filename)
    return job_file_basename[:-1*'.json'.__len__()]


def get_timestamp():
    return time.strftime('%Y%m%d', time.localtime(time.time()))


def make_job_result_dir(job_filename, result_dir):
    job_name = get_job_name(job_filename)
    job_result_dir = os.path.join(result_dir, get_timestamp(), job_name)
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


def main():
    job_dir = 'C:/Users/wengm/Projects/StockAnt/test/job'
    result_dir = 'C:/Users/wengm/Projects/StockAnt/test/result'
    job_files = get_job_files(job_dir)
    for job_file in job_files:
        job_result_dir = make_job_result_dir(job_file, result_dir)
        print(job_result_dir)
        backtest.backtest(job_file, job_result_dir)


if __name__ == "__main__":
    main()
