# coding:utf-8
from data.history_daily_provider import HistoryDailyProvider
import utils.parser

code = 'hs300'
start_date = utils.parser.parse_date('2010-01-01')
end_date = utils.parser.parse_date('2016-10-28')
output_dir = 'D:\\working\\StockAnt\\backtest\\result\\'
data_df = HistoryDailyProvider.get_data(code, start_date, end_date)
data_df.to_csv(output_dir + code + '.csv', index=False)
