import pandas as pd


def find(one_series, start_offset, end_offset, look_for_value):
    output_arr = []
    for i in range(0, len(one_series)):
        start_index = i + start_offset
        end_index = i + end_offset
        if start_index < 0 or end_index < 0:
            output_arr.append(None)
            continue
        count = 0
        for j in range(start_index, end_index+1):
            value = one_series[j]
            if value == look_for_value:
                count += 1
        output_arr.append(count)
    return pd.Series(output_arr)
