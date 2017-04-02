# coding:utf-8
import json
import os
import types
from data.stock_hfq_daily_provider import StockHfqDailyProvider
from data.stock_basic_provider import StockBasicProvider
import utils.parser
import utils.reflect
import pandas as pd
import math


def backtest(job_filename, result_dir):
    # Load the job define file
    job_file = file(job_filename)
    job = json.load(job_file, 'utf-8')
    job = encode_json(job, 'utf-8')
    # Define something
    trade_dfs = []
    benchmark_df = init_benchmark_df(job['benchmark'])
    # Parse the date section
    start_date = utils.parser.parse_date(job['start_date'])
    end_date = utils.parser.parse_date(job['end_date'])
    # Parse the stock filter then get the stock set
    stock_codes = stock_filter(job['stock_filter'].decode('utf-8'))
    # Loop the stocks
    done = 0
    for stock_code in stock_codes:
        print(stock_code)
        if not StockBasicProvider.can_trade(stock_code):
            continue
        # Calculate the series
        stock_df = StockHfqDailyProvider.get_data(stock_code, start_date, end_date)
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
        # Trading
        trade_define = job['trade']
        trade_method_name = trade_define['method']
        trade_method_args = build_args(trade_define['method_args'], stock_df, job['params'])
        trade_df = utils.reflect.apply_func(trade_method_name, trade_method_args)
        trade_df.insert(loc=0, column="code", value=stock_code)
        trade_dfs.append(trade_df)
        # Benchmark
        for benchmark_define in job['benchmark']:
            method_name = benchmark_define['method']
            method_args = build_args(benchmark_define['method_args'], trade_df, job['params'])
            method_args['trade_df'] = trade_df
            output = utils.reflect.apply_func(method_name, method_args)
            output_names = benchmark_define['name'].split(',')
            benchmark_df.set_value(done, 'code', stock_code)
            if len(output_names) == 1:
                benchmark_df.set_value(index=done, col=output_names[0], value=output)
            else:
                for i in range(0, len(output_names)):
                    benchmark_df.set_value(index=done, col=output_names[i], value=output[i])
        done += 1
        # if done > 10:
        #    break
        print(done)
    # Save the trade result
    pd.concat(trade_dfs).to_csv(os.path.join(result_dir, 'trade.csv'), index=False)
    # Save the benchmark result
    benchmark_df.to_csv(os.path.join(result_dir, 'benchmark.csv'), index=False)
    return


def init_benchmark_df(benchmark_defines):
    column_names = ['code']
    for benchmark_define in benchmark_defines:
        names = benchmark_define['name'].split(',')
        for name in names:
            column_names.append(name)
    return pd.DataFrame(columns=column_names)


def stock_filter(filter_str):
    split_pos = filter_str.find(':')
    if split_pos > 0:
        filter_values = filter_str.split(':')
        if len(filter_values) == 2:
            filter_category = filter_values[0]
            filter_category_names = filter_values[1].split(',')
        else:
            print('Invalid stock filter')
            return
    else:
        filter_values = filter_str.split(',')
        is_stock_codes = True
        for filter_value in filter_values:
            for c in range(0, len(filter_value)):
                if not ('0' <= c <= '9'):
                    is_stock_codes = False
                    break
            if not is_stock_codes and len(filter_values) > 1:
                print('Invalid stock filter')
                return
        if len(filter_values) == 1:
            filter_category = filter_values[0]
            filter_category_names = None
        else:
            filter_category = None
            filter_category_names = filter_values
    return StockBasicProvider.find_codes(filter_category, filter_category_names)


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


def encode_json(input, encoding):
    if isinstance(input, dict):
        return {encode_json(key, encoding): encode_json(value, encoding) for (key, value) in input.items()}
    elif isinstance(input, list):
        return [encode_json(element, encoding) for element in input]
    elif isinstance(input, unicode):
        return input.encode(encoding)
    else:
        return input


if __name__ == "__main__":
    backtest('C:/Users/wengm/Projects/StockAnt/test/job/bias2.json', 'C:/Users/wengm/Projects/StockAnt/test/job/')
