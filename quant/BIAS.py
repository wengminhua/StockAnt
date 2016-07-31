import pandas as pd
import utils.Valid


def bias(close_series, ma_series):
    output_arr = []
    for i in range(0, len(close_series)):
        close = close_series[i]
        ma = ma_series[i]
        if utils.Valid.isValidNumbers([close, ma]):
            output_arr.append(((close - ma) / ma) * 100)
        else:
            output_arr.append(None)
    return pd.Series(output_arr)
