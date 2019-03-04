# welcome to the user's guide.<br>
## Overview
This program is designed to play with the critical data of China A share. It serves as a **tool for stock selection**.<br>
Here are two major pieces of code<br>
* [ChinaAShare/main.py](https://github.com/broken1999/ChinaAShare/blob/master/main.py) is the main tool
* [ChinaAshare/retrieve_2015_data/retrieve2015data.py](https://github.com/broken1999/ChinaAShare/blob/master/retrieve_2015_data/retrieve2015data.py) is the program used to download the highest price (前复权) of 2015. The year 2015 is chosen, because A share had a peak by then which now can be used as the ceiling of growth.

## Prerequisites
Anaconda Python 3, Numpy, Pandas, [TuShare](https://pypi.org/project/tushare/)

## Details of [ChinaAShare/main.py](https://github.com/broken1999/ChinaAShare/blob/master/main.py)
1. Run [ChinaAShare/main.py](https://github.com/broken1999/ChinaAShare/blob/master/main.py) in Python 3. The most [recent daily data](https://tushare.pro/document/2?doc_id=27) will be loaded into memory and a copy of it will be saved on disk with name \*.pkl.<br>
2. Now we can play with the data stored in the variable called `ctb` and `basics`.<br>

#### Play with price-book value ratio (PB)
* Sample input and output:<br>
`PB_rangemin=0.01`<br>
`PB_rangemax=0.5`<br>
`PB(ctb,PB_rangemin,PB_rangemax)`<br>
>002680  \*ST长生     生物制药   1.56   3.85  0.405195<br>
>002354   天神娱乐      互联网   4.74  10.11  0.468843<br>
>002501   利源精制        铝   2.83   5.80  0.487931<br>
>002122  \*ST天马     机械基件   1.88   3.80  0.494737<br>
* Variables, functions and parameters explained: <br> 
`ctb` today's data. [details](http://tushare.org/trading.html#id4) <br>
`basics` basic data of stocks. [details](http://tushare.org/trading.html#id3) <br>
`PB()` a simple function to return the list of stocks with PB ratio falls in the range \[PB_rangemin,PB_rangemax\) <br>
`PB_rangemin` the minimum of price-book value ratio, a selection criterion <br>
`PB_rangemax` the maximum of price-book value ratio, a selection criterion <br>


## Details of [ChinaAshare/retrieve_2015_data/retrieve2015data.py](https://github.com/broken1999/ChinaAShare/blob/master/retrieve_2015_data/retrieve2015data.py)
1. One does **NOT** need to run [ChinaAshare/retrieve_2015_data/retrieve2015data.py](https://github.com/broken1999/ChinaAShare/blob/master/retrieve_2015_data/retrieve2015data.py). The program is designed to download the stock data of 2015 to the hard disk, named as HighPoint2015.pkl, which is readily given in the Github folder [ChinaAshare/retrieve_2015_data/](https://github.com/broken1999/ChinaAShare/blob/master/retrieve_2015_data/).
2. Nevertheless, one could change the date range in the [ChinaAshare/retrieve_2015_data/retrieve2015data.py](https://github.com/broken1999/ChinaAShare/blob/master/retrieve_2015_data/retrieve2015data.py) to get data of years other than 2015.
* Sample input and output: no input needed; output is file HighPoint2015.pkl
* Variables, functions and parameters explained:<br>
`Time_rangemin` the start date of data retrieval<br>
`Time_rangemax` the end date of data retrieval<br>




#### this is test of overwrite