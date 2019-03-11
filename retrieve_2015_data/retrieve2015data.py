import os
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import tushare as ts
import datetime

#ts.set_token('09f77414f088aad7959f5eecba391fe685ea50462e208ce451b1b6a6')
pro = ts.pro_api('09f77414f088aad7959f5eecba391fe685ea50462e208ce451b1b6a6')
StockBasic = pro.query('stock_basic', list_status='L')

# 主板，20151231前上市，
stockcodepool = StockBasic[(StockBasic['list_date']<'20151231') & (StockBasic['market']=='主板')]

# find the peak value of stock price in year 2015
Time_rangemin='20150101'
Time_rangemax='20151231'

# date of today and adjustment factors
todaydate=datetime.datetime.today().strftime('%Y%m%d')
#AdjustmentFactorToday = pro.adj_factor(ts_code='', trade_date=todaydate)
#AdjustmentFactorTimeRangeMax = pro.adj_factor(ts_code='', trade_date=Time_rangemax)

HighPoint2015 = pd.DataFrame(columns=['ts_code', 'HighPoint2015'])
for ts_code in stockcodepool['ts_code']:
    print(ts_code)
    # 未复权
    # temp = pro.monthly(ts_code=ts_code, start_date=Time_rangemin, end_date=Time_rangemax,fields='ts_code, high')
    try:
        # 伪前复权， 当日收盘价 × 当日复权因子 / 20151231复权因子
        # 前复权， 当日收盘价 × 当日复权因子 / 20151231复权因子 × (20151231复权因子 / 最新复权因子)
        # 这里使用不复权价格，配合复权因子
        quote = ts.pro_bar(pro_api=pro, ts_code=ts_code, freq='D', adj=None , start_date=Time_rangemin, end_date=Time_rangemax )
        HighPoint = quote['high'].max()
        HighPointDate = quote.at[quote[quote['high']== HighPoint].index[0],'trade_date']
        AdjustmentFactorHighPointDate = pro.adj_factor(ts_code=ts_code, trade_date=HighPointDate)
        HighPoint2015 = HighPoint2015.append(pd.DataFrame({'ts_code':[ts_code], 'HighPoint2015': [HighPoint], 'AdjustmentFactorHighPointDate':[AdjustmentFactorHighPointDate.at[0,'adj_factor']]}), ignore_index=True, sort=True)
    except TypeError:
        continue

HighPoint2015.to_pickle('HighPoint'+Time_rangemin+Time_rangemax+'.pkl')