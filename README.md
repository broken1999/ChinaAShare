# ChinaAShare
based on history, focused on present
## The aim of this project:
* Spot the ideal target of investment in `China A share` stock exchange market.
* Reduce the manual effort using Python program.  
## Current features:
* retrieve daily quote. [details](http://tushare.org/trading.html#id4)
> code：代码
> name:名称
> changepercent:涨跌幅
> trade:现价
> open:开盘价
> high:最高价
> low:最低价
> settlement:昨日收盘价
> volume:成交量
> turnoverratio:换手率
> amount:成交金额
> per:市盈率
> pb:市净率
> mktcap:总市值
> nmc:流通市值
* retrieve the quote in year 2015. [details](http://tushare.org/trading.html#id2) Especially the highest stock price before the crash.
## Strategy
* The quotient of highest price in 2015 and current price is seen as the room for growth.
* Price book value ratio is seen as an indicator of valuation.
## Possible future features:
#### Planned:
* comparison to industry average
#### nice to have
* data visualization, e.g. [heat map](https://github.com/FrankBGao/HeatMap_for_TuShare).
### Programming packages/projects involed:
[TuShare](http://tushare.org); Anaconda (Pandas, Numpy)
