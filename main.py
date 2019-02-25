import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import tushare as ts
import matplotlib.pyplot as plt


def tbt(ctb, lowlim=0, upplim=1):
    ## (trade-bvps)/trade=btt
    ## np.sign(NaN) will generate warning "RuntimeWarning: invalid value encountered in sign"
    btt = Series((ctb['trade'] - ctb['bvps']) / ctb['trade'], index=ctb.index.values, name='btt')
    ## code, trade, bvps, (bvps-trade)/bvps=btb
    ctbbtt = pd.concat([ctb, btt], axis=1)
    return ctbbtt[(ctbbtt['btt'] >= lowlim) & (ctbbtt['btt'] < upplim)].sort_values(['btt'])

# PB price-book value ratio
def PB(ctb, lowlim=0, upplim=np.inf):
    ## trade/bvps=PB
    ## np.sign(NaN) will generate warning "RuntimeWarning: invalid value encountered in sign"
    PB = Series(ctb['trade'] / ctb['bvps'], index=ctb.index.values, name='PB')
    ## code, trade, bvps, trade/bvps=PB
    ctbtb = pd.concat([ctb, PB], axis=1)
    return ctbtb[(ctbtb['PB'] >= lowlim) & (ctbtb['PB'] < upplim)].sort_values(['PB'])


## load data
refresh = 1

if refresh:
    ## today quotation
    td = ts.get_today_all()
    td.to_pickle('td.pkl')
    ## performance
    yj = ts.get_report_data(2017, 3)
    yj.to_pickle('yj.pkl')
    ## basics
    basics = ts.get_stock_basics()
    basics.to_pickle('basics.pkl')
if (1 - refresh):
    td = pd.read_pickle('td.pkl')
    yj = pd.read_pickle('yj.pkl')
    basics = pd.read_pickle('basics.pkl')

## construct dataframe code, trade, bvps
trade = td[['code', 'trade']].set_index('code')
bvps = basics['bvps'].to_frame()
name = basics[['name', 'industry']]  # .to_frame()
#name.drop_duplicates(keep=False,inplace=True)
name.drop_duplicates(keep=False)
ctb = pd.concat([name, trade[~trade.index.duplicated(keep='first')], bvps], axis=1)


###### PB, price-book value ratio, selection
PB_rangemin=0.01
PB_rangemax=0.5
PBselection=td[ (td['pb']>PB_rangemin) & (td['pb'] <PB_rangemax)].sort_values(['pb'])
