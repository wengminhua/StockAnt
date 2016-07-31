import pandas as pd


def series_and(series_arr):
    output_arr = []
    for i in range(0, len(series_arr[0])):
        and_result = True
        for series in series_arr:
            if series[i] is None:
                and_result = None
                break
            elif not series[i]:
                and_result = False
                continue
        output_arr.append(and_result)
    return pd.Series(output_arr)


def series_or(series_arr):
    output_arr = []
    for i in range(0, len(series_arr[0])):
        or_result = False
        for series in series_arr:
            if series[i] is None:
                or_result = None
                break
            elif series[i]:
                or_result = True
                continue
        output_arr.append(or_result)
    return pd.Series(output_arr)
