import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import tushare as ts
import matplotlib.pyplot as plt
import datetime

tspro = ts.pro_api('09f77414f088aad7959f5eecba391fe685ea50462e208ce451b1b6a6')
StockBasic = tspro.query('stock_basic', list_status='L')
HighPoint2015 = pd.read_pickle('retrieve_2015_data/HighPoint2015010120151231.pkl')
todaydate = datetime.datetime.today().strftime('%Y%m%d')

###### load today data
refresh = 1

if refresh:
    ## today quotation
    # td = ts.get_today_all()
    td = tspro.daily_basic(trade_date=todaydate)
    td.to_pickle('td' + todaydate + '.pkl')

    # today's adjustment factors
    AdjustmentFactorToday = tspro.adj_factor(ts_code='', trade_date=todaydate)
    AdjustmentFactorToday = AdjustmentFactorToday.set_index('ts_code')
    AdjustmentFactorToday = AdjustmentFactorToday.sort_index()
    AdjustmentFactorToday = AdjustmentFactorToday.rename(columns={'adj_factor':'AdjustmentFactorToday'})
    AdjustmentFactorToday.to_pickle('AdjustmentFactorToday' + todaydate + '.pkl')

if (1 - refresh):
    td = pd.read_pickle('td' + todaydate + '.pkl')
    AdjustmentFactorToday = AdjustmentFactorToday.read_pickle('AdjustmentFactorToday' + todaydate + '.pkl')


###### prepare HighPoint2015vclose
td = td.set_index('ts_code')
td = td.sort_index()
HighPoint2015 = HighPoint2015.set_index('ts_code')
HighPoint2015 = HighPoint2015.sort_index()

tdwHighPoint2015 = pd.concat([td, HighPoint2015, AdjustmentFactorToday, StockBasic.set_index('ts_code')], axis=1, join='inner')

tdwHighPoint2015['HighPoint2015vclose'] = tdwHighPoint2015['HighPoint2015'] * tdwHighPoint2015[
    'AdjustmentFactorHighPointDate'] / tdwHighPoint2015['AdjustmentFactorToday'] / tdwHighPoint2015['close']


###### PB, price-book value ratio, selection
PB_rangemin = 0.01
PB_rangemax = 0.5
PBselection = td[(td['pb'] > PB_rangemin) & (td['pb'] < PB_rangemax)].sort_values(['pb'])


###### selection based on 'HighPoint2015vclose' and 'pb'
PB_rangemin = 0.01
PB_rangemax = 1
HighPoint2015vclose_rangemin = 5
HighPoint2015vclose_rangemax = 10
selection=tdwHighPoint2015[ (tdwHighPoint2015['HighPoint2015vclose']>HighPoint2015vclose_rangemin) & (tdwHighPoint2015['HighPoint2015vclose']<HighPoint2015vclose_rangemax) & (tdwHighPoint2015['pb']>PB_rangemin) & (tdwHighPoint2015['pb']<PB_rangemax) ]
print(selection[['name','industry','pb','HighPoint2015vclose']])
