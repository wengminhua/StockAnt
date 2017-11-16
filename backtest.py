# coding:utf-8
import json
import os
import types
from data.stock_hfq_daily_provider import StockHfqDailyProvider
from data.stock_basic_provider import StockBasicProvider
from data.index_basic_provider import IndexBasicProvider
from data.index_daily_provider import IndexDailyProvider
import utils.parser
import utils.reflect
import pandas as pd
import sys
import getopt
from mpi4py import MPI

g_comm = MPI.COMM_WORLD
g_comm_rank = g_comm.Get_rank()
g_comm_size = g_comm.Get_size()


def backtest(job_filename, result_dir, start_date=None, end_date=None):
    # Load the job define file
    job_file = file(job_filename)
    job = json.load(job_file, 'utf-8')
    job = encode_json(job, 'utf-8')
    # Define something
    trade_dfs = []
    benchmark_df = init_benchmark_df(job['benchmark'])
    # Parse the date section
    if start_date is None:
        start_date = utils.parser.parse_date(job['start_date'])
    if end_date is None:
        end_date = utils.parser.parse_date(job['end_date'])
    # Parse the stock filter then get the stock set
    filter_category, filter_category_names = parse_code_filter(job['code_filter'].decode('utf-8'))
    if filter_category is None and filter_category_names is None:
        return
    if job['code_type'] == "stock":
        backtest_basic_provider = StockBasicProvider
        backtest_daily_provider = StockHfqDailyProvider
    elif job['code_type'] == "index":
        backtest_basic_provider = IndexBasicProvider
        backtest_daily_provider = IndexDailyProvider
    else:
        print "Invalid code type"
        return None
    backtest_codes = backtest_basic_provider.find_codes(filter_category, filter_category_names)
    # Loop the stocks
    global_count = 0
    count = 0
    for backtest_code in backtest_codes:
        global_count += 1
        if global_count % g_comm_size == g_comm_rank:
            count += 1
        else:
            continue
        print("Process %d: %s" % (global_count, backtest_code))
        if not backtest_basic_provider.can_trade(backtest_code):
            continue
        # Calculate the series
        stock_df = backtest_daily_provider.get_data(backtest_code, start_date, end_date)
        for series_define in job['series']:
            method_name = series_define['method']
            method_args = build_args(series_define['method_args'], stock_df, job['params'])
            output = utils.reflect.apply_func(method_name, method_args)
            output_names = series_define['name'].split(',')
            if len(output_names) == 1:
                stock_df.insert(loc=len(stock_df.columns), column=output_names[0], value=output)
            else:
                for i in range(0, len(output_names)):
                    stock_df.insert(loc=len(stock_df.columns), column=output_names[i], value=output[i])
        stock_df.to_csv(os.path.join(result_dir, backtest_code + '.csv'), index=False)
        # Trading
        trade_define = job['trade']
        trade_method_name = trade_define['method']
        trade_method_args = build_args(trade_define['method_args'], stock_df, job['params'])
        trade_df = utils.reflect.apply_func(trade_method_name, trade_method_args)
        trade_df.insert(loc=0, column="code", value=backtest_code)
        trade_dfs.append(trade_df)
        # Benchmark
        for benchmark_define in job['benchmark']:
            method_name = benchmark_define['method']
            method_args = build_args(benchmark_define['method_args'], trade_df, job['params'])
            method_args['stock_df'] = stock_df
            method_args['trade_df'] = trade_df
            output = utils.reflect.apply_func(method_name, method_args)
            output_names = benchmark_define['name'].split(',')
            benchmark_df.at[count, 'code'] = backtest_code
            if len(output_names) == 1:
                benchmark_df.at[count, output_names[0]] = output
            else:
                for i in range(0, len(output_names)):
                    benchmark_df.at[count, output_names[i]] = output[i]
    # Save the trade result
    if g_comm_rank == 0:
        for source in range(1, g_comm_size):
            temp_dfs = g_comm.recv(source=source, tag=10)
            trade_dfs.extend(temp_dfs)
        pd.concat(trade_dfs).to_csv(os.path.join(result_dir, 'trade.csv'), index=False)
    else:
        g_comm.send(trade_dfs, dest=0, tag=10)
    # Save the benchmark result
    if g_comm_rank == 0:
        benchmark_dfs = [benchmark_df]
        for source in range(1, g_comm_size):
            temp_df = g_comm.recv(source=source, tag=20)
            benchmark_dfs.append(temp_df)
        pd.concat(benchmark_dfs).to_csv(os.path.join(result_dir, 'benchmark.csv'), index=False)
    else:
        g_comm.send(benchmark_df, dest=0, tag=20)
    return


def init_benchmark_df(benchmark_defines):
    column_names = ['code']
    for benchmark_define in benchmark_defines:
        names = benchmark_define['name'].split(',')
        for name in names:
            column_names.append(name)
    return pd.DataFrame(columns=column_names)


def parse_code_filter(code_filter):
    split_pos = code_filter.find(':')
    if split_pos > 0:
        filter_values = code_filter.split(':')
        if len(filter_values) == 2:
            filter_category = filter_values[0]
            filter_category_names = filter_values[1].split(',')
        else:
            print('Invalid code filter')
            return None
    else:
        filter_values = code_filter.split(',')
        is_codes = True
        for filter_value in filter_values:
            for c in range(0, len(filter_value)):
                if not ('0' <= filter_value[c] <= '9'):
                    is_codes = False
                    break
            if not is_codes and len(filter_values) > 1:
                print('Invalid code filter')
                return None
        if len(filter_values) == 1:
            filter_category = filter_values[0]
            filter_category_names = None
        else:
            filter_category = None
            filter_category_names = filter_values
    return filter_category, filter_category_names


def build_args(args_dict, stock_df, params_dict):
    another_args_dict = dict()
    for (arg_key, arg_value) in args_dict.items():
        if isinstance(arg_value, types.StringTypes):
            another_args_dict[arg_key] = build_single_arg(arg_value, stock_df, params_dict)
        elif isinstance(arg_value, list):
            another_list = list()
            for i in range(0, len(arg_value)):
                another_list.append(build_single_arg(arg_value[i], stock_df, params_dict))
            another_args_dict[arg_key] = another_list
        elif isinstance(arg_value, dict):
            another_dict = dict()
            for (temp_key, temp_value) in arg_value.items():
                another_dict[temp_key] = build_single_arg(arg_value[temp_key], stock_df, params_dict)
            another_args_dict[arg_key] = another_dict
        else:
            another_args_dict[arg_key] = arg_value
    return another_args_dict


def build_single_arg(arg_value, stock_df, params_dict):
    if arg_value.startswith('%') and arg_value.endswith('%'):
        param_key = arg_value[1:len(arg_value)-1]
        return params_dict[param_key]
    if arg_value.startswith('[') and arg_value.endswith(']'):
        inner_value = arg_value[1:len(arg_value)-1]
        series_name = get_temp_series_name()
        if inner_value.startswith('%') and inner_value.endswith('%'):
            param_key = inner_value[1:len(inner_value)-1]
            stock_df.insert(loc=len(stock_df.columns), column=series_name, value=params_dict[param_key])
        else:
            temp = parse_str_value(inner_value)
            if temp is not None:
                stock_df.insert(loc=len(stock_df.columns), column=series_name, value=temp)
            else:
                series_name = inner_value
        return stock_df[series_name]
    temp = parse_str_value(arg_value)
    if temp is not None:
        return temp
    return arg_value


def parse_str_value(str_value):
    temp = utils.parser.parse_number(str_value)
    if temp is not None:
        return temp
    temp = utils.parser.parse_bool(str_value)
    if temp is not None:
        return temp
    return None


temp_series_id = 0


def get_temp_series_name():
     global temp_series_id
     temp_series_id += 1
     return 'SYS_%d' % temp_series_id


def encode_json(input_value, encoding):
    if isinstance(input_value, dict):
        return {encode_json(key, encoding): encode_json(value, encoding) for (key, value) in input_value.items()}
    elif isinstance(input_value, list):
        return [encode_json(element, encoding) for element in input_value]
    elif isinstance(input_value, unicode):
        return input_value.encode(encoding)
    else:
        return input_value


def main(argv=None):
    if argv is None:
        argv = sys.argv
    options, args = getopt.getopt(argv[1:], "s:r:", ["strategy=", "result="])
    for name, value in options:
        if name in ("-s", "--strategy"):
            strategy_filename = value
        if name in ("-r", "--result"):
            result_path = value
    backtest(strategy_filename, result_path)

if __name__ == "__main__":
    sys.exit(main())
