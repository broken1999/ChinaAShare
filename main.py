import os
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import tushare as ts
import matplotlib.pyplot as plt
import datetime

#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

tspro = ts.pro_api('09f77414f088aad7959f5eecba391fe685ea50462e208ce451b1b6a6')
StockBasic = tspro.query('stock_basic', list_status='L')
HighPoint2015 = pd.read_pickle('retrieve_2015_data/HighPoint2015010120151231.pkl')
todaydate = datetime.datetime.today().strftime('%Y%m%d')

def normalize( value, value_min, value_max ):
    normalized_value=((value-value_min)/(value_max-value_min))
    return normalized_value


###### load today data
refresh = 1

# change date to most recent working day if today is holiday/ weekend
holidays=['20190101','20190204','20190205','20190206','20190207','20190208','20190405','20190501','20190607','20190913','20191001','20191002','20191003','20191004','20191007']
weekday=datetime.datetime.today().weekday()
while (weekday == 5) or (weekday == 6) or (todaydate in holidays):
    # find the most recent working date
    todaydate=str(int(todaydate)-1)
    weekday = datetime.date(int(todaydate[0:4]), int(todaydate[4:6]), int(todaydate[6:8])).weekday()

# not refresh when file exists and valid
if os.path.exists('td' + todaydate + '.pkl'):
    if os.stat('td' + '20190405' + '.pkl').st_size > 1000:
        refresh = 0

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

###### refresh financial indicators

refresh = 0
financialindicatorreportperiod = '20181231'

if refresh:
    ## prepare financial indicators
    FinancialIndicators = pd.DataFrame()
    for ts_code in StockBasic['ts_code']:
        financialindicator = tspro.fina_indicator(ts_code=ts_code, period=financialindicatorreportperiod)
        FinancialIndicators = FinancialIndicators.append(financialindicator)

    FinancialIndicators = FinancialIndicators.set_index('ts_code')
    FinancialIndicators.to_pickle('FinancialIndicators' + financialindicatorreportperiod + '.pkl')

if (1 - refresh):
    FinancialIndicators = pd.read_pickle('FinancialIndicators' + financialindicatorreportperiod + '.pkl')


###### export today quote + financial indicators Excel
tdwFinancialIndicators = pd.concat([td.set_index('ts_code'), FinancialIndicators], axis=1, join='outer', sort=True)
tdwFinancialIndicators.to_excel("TodayQuote_FinancialIndicators"+todaydate+".xlsx")


###### prepare HighPoint2015vclose
td = td.set_index('ts_code')
td = td.sort_index()
HighPoint2015 = HighPoint2015.set_index('ts_code')
HighPoint2015 = HighPoint2015.sort_index()

tdwHighPoint2015 = pd.concat([td, HighPoint2015, AdjustmentFactorToday, StockBasic.set_index('ts_code')], axis=1, join='outer', sort=True)

tdwHighPoint2015['HighPoint2015vclose'] = tdwHighPoint2015['HighPoint2015'] * tdwHighPoint2015[
    'AdjustmentFactorHighPointDate'] / tdwHighPoint2015['AdjustmentFactorToday'] / tdwHighPoint2015['close']

#######selection_output = selection[['name','industry','HighPoint2015vclose','HighPoint2015vclose_IndustrialPercentage','pb','pb_IndustrialPercentage','pe']]
print(selection_output)
selection_output.to_excel("HighPoint2015_PB_PE_selected_"+todaydate+".xlsx")


###### normalize the values into percentage according to industries
tdwHighPoint2015wIndustrialPercentage=pd.DataFrame()

ListofIndustries=tdwHighPoint2015['industry'].drop_duplicates().to_string(index=False).split()
ListofIndicators=['pb','pe','HighPoint2015vclose']
for industryname in ListofIndustries[1:]:
    tobenormalized=tdwHighPoint2015[tdwHighPoint2015['industry']==industryname]
    for indicatorname in ListofIndicators:
        oneindicatornormalized=[]
        for onevalueofoneindicator in tobenormalized[indicatorname]:
            oneindicatornormalized.append(normalize(onevalueofoneindicator, tobenormalized[indicatorname].min(), tobenormalized[indicatorname].max()))
        tobenormalized[indicatorname+'_IndustrialPercentage']=oneindicatornormalized
    tdwHighPoint2015wIndustrialPercentage=pd.concat([tdwHighPoint2015wIndustrialPercentage,tobenormalized])
tdwHighPoint2015wIndustrialPercentage=tdwHighPoint2015wIndustrialPercentage.sort_index()

tdwHighPoint2015wIndustrialPercentage_fulllistoutput=tdwHighPoint2015wIndustrialPercentage[['name','industry','HighPoint2015vclose','HighPoint2015vclose_IndustrialPercentage','pb','pb_IndustrialPercentage','pe']]
tdwHighPoint2015wIndustrialPercentage_fulllistoutput.to_excel("HighPoint2015_PB_PE_fulllist"+todaydate+".xlsx")


###### selection based on 'pb_IndustrialPercentage' and 'HighPoint2015vclose_IndustrialPercentage'
pb_rangemin = -np.inf
pb_rangemax = np.inf
pb_IndustrialPercentage_rangemin = -np.inf
pb_IndustrialPercentage_rangemax =  np.inf
HighPoint2015vclose_rangemin = -np.inf
HighPoint2015vclose_rangemax = np.inf
HighPoint2015vclose_IndustrialPercentage_rangemin = -np.inf
HighPoint2015vclose_IndustrialPercentage_rangemax =  np.inf
selection = tdwHighPoint2015wIndustrialPercentage[
                     (tdwHighPoint2015wIndustrialPercentage['pb'] >= pb_rangemin)
                   & (tdwHighPoint2015wIndustrialPercentage['pb'] <= pb_rangemax)
                   & (tdwHighPoint2015wIndustrialPercentage['pb_IndustrialPercentage'] >= pb_IndustrialPercentage_rangemin)
                   & (tdwHighPoint2015wIndustrialPercentage['pb_IndustrialPercentage'] <= pb_IndustrialPercentage_rangemax)
                   & (tdwHighPoint2015wIndustrialPercentage['HighPoint2015vclose'] >= HighPoint2015vclose_rangemin)
                   & (tdwHighPoint2015wIndustrialPercentage['HighPoint2015vclose'] <= HighPoint2015vclose_rangemax)
                   & (tdwHighPoint2015wIndustrialPercentage['HighPoint2015vclose_IndustrialPercentage'] >= HighPoint2015vclose_IndustrialPercentage_rangemin)
                   & (tdwHighPoint2015wIndustrialPercentage['HighPoint2015vclose_IndustrialPercentage'] <= HighPoint2015vclose_IndustrialPercentage_rangemax)]
selection_output = selection[['name','industry','HighPoint2015vclose','HighPoint2015vclose_IndustrialPercentage','pb','pb_IndustrialPercentage','pe']]
print(selection_output)
selection_output.to_excel("HighPoint2015_PB_PE_selected_"+todaydate+".xlsx")



