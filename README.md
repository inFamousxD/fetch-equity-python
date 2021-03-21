# fetch-equity-python
Test repository to fetch equity data for NSE:COFFEEDAY with 2 year (dyanamic) timeframe.

Prerequisites : alpha_vantage, pandas.
```bash
pip3 install alpha_vantage pandas

python3 fetch-equity.py
```
Outputs: 
```bash
Printing data from 2018-06-10 up until 2020-06-10

             1. open   2. high    3. low  4. close  5. volume
date                                                         
2020-06-09   15.6500   15.6500   15.6500   15.6500        0.0
2020-06-08   15.6439   15.6549   15.6336   15.6500   880740.0
2020-06-05   15.6610   15.6677   15.6019   15.6439   544033.0
2020-06-04   15.6708   15.6952   15.6296   15.6610     4640.0
2020-06-03   15.5861   15.7797   15.5690   15.6708   499942.0
...              ...       ...       ...       ...        ...
2018-06-15  304.0000  314.0000  302.0000  305.1000   351966.0
2018-06-14  295.7000  309.0000  291.2500  304.7500   336372.0
2018-06-13  304.7000  306.0000  293.0000  294.4500   188530.0
2018-06-12  312.0000  315.1000  299.0000  303.5000   245928.0
2018-06-11  285.0000  333.0000  285.0000  310.8500  1389405.0
[486 rows x 5 columns]
```
# A Python module for fetching and processing stock data through APIs

## Pre-requisites

### Python modules
#### API
- yfinance
- nsetools
- bsedata
- alphavantage

#### Other
- matplotlib
- numpy
- pandas
- pymongo
- seaborn

## Overview
Import the file equity_data.py into your project. There are 3 inherent classes : 
- FetchData
- ProcessData
- MongoFrame

### FetchData
Methods `fetchSymbols` and `fetchEquityData` make up class FetchData.

#### fetchSymbols method
`fetchSymbols(self, exchangeType, path=None)`

This method takes `exchangeType` and `path` (optional) as arguments to fetch stock symbols or 'Tickers'. NSE and BSE tickers are auto fetched by modules `nsetools` and `bsedata`.
Symbols other than the one's metioned above are to be fetched from a .csv file where the `path` variable comes into picture.


##### Code to fetch all NSE tickers from nsetools API.
```py
from equity_data import FetchData

fe = FetchData()

nseTickers = fe.fetchSymbols('nse')
```

#### fetchEquityData method
`fetchEquityData(self, symbol, period=None, duration=None)`

This method takes `symbol` (ticker symbol compatible with yfinance), `period` (period to download data of. Ranges from '1d', '1mo', '1y', '5y', 'max') and `duration` (duration to download data of. Takes an array of datetime objects.) Returns a `pandas DataFrame` object.

##### Code to fetch dataframe for ADANIPORTS.NS for 1 year period and 1 year duration.
```py
df_1 = fe.fetchEquityData('ADANIPORTS.NS', period='1y')
df_2 = fe.fetchEquityData('ADANIPORTS.NS', duration=['2015-01-01', '2016-01-01'])
```

printing df_1 returns : 

```bash
                  Open        High         Low       Close   Adj Close   Volume
Date                                                                           
2019-07-10  406.950012  408.799988  402.350006  405.000000  400.362396  2023029
2019-07-11  408.200012  413.700012  403.899994  412.899994  408.171936  1732979
2019-07-12  411.950012  419.399994  409.600006  415.299988  410.544403  2818537
2019-07-15  413.549988  416.200012  408.100006  409.100006  404.415436  2601603
2019-07-16  411.649994  421.500000  407.649994  417.750000  412.966370  2111513
...                ...         ...         ...         ...         ...      ...
2020-07-06  365.100006  366.000000  356.100006  359.450012  359.450012  3360559
2020-07-07  361.000000  361.000000  344.250000  345.950012  345.950012  4348413
2020-07-08  349.000000  349.649994  339.299988  340.600006  340.600006  3988463
2020-07-09  341.000000  346.500000  340.000000  343.149994  343.149994  3635224
2020-07-10  341.000000  342.700012  332.250000  334.950012  334.950012  3368106

[245 rows x 6 columns]
```

Output is consistent for all symbols while using yfinance API.

### ProcessData
Methods `performPolyFit`, `createDataFrame` and `findMinMax` make up class ProcessData.

#### performPolyFit method

`performPolyFit(self, data, plot=False, ordinalise=True)`

This methoda takes `data` which is a pandas DataFrame object recieved from yfinance API, `plot` - a Boolean variable when set to True plots the dataframe with a regression line using `seaborn` library, `ordinalise` - another Boolean variable when set to true ordinalises date index in the dataframe so a polyfit could be performed on 'Date' and 'Adjusted Close'.

This method returns `slope, intercept, dataframe` where dataframe is ordinalised.

```py
from equity_data import ProcessData
pe = ProcessData()

slope, intercept, df = pe.performPolyFit(df, plot=True, ordinalise=True)
```

#### createDataFrame method

`createDataFrame(self, codeList, exchangeType=None, path=None, period=None, duration=[], limit=None, normaliser='mean')`

This method aims at taking a list of Tickers from the user and creating a dataframe of all the Tickers which includes the Returns and Volatility in a single pandas DataFrame object. It uses performPolyFit method to get slope, intercept - calculates volatility, normalises the data and passes the dataframe back.

Arguments include `codeList` which is a list of tickers under a single exchange where `exchangeType` specifies this exchange along with the `path` to save the eccentric values into. It takes same arguments as `period` and `duration` to `performPolyFit` and `fetchEquityData` methods. It auto downloads data and performs the above actions.
Additionally - a `limit` variable is set to limit the number of tickers from the list of Tickers, also a `normaliser` type which normalises the entire 'Adj Close' column by either `mean`, `recent` or `oldest` price.

```py
tickerArray = fe.fetchSymbols('nse')

df = pe.createDataFrame(tickerArray, limit=100, exchangeType='nse', period='1y', normaliser='oldest', path=/some/path)
```

#### findMinMax method

`findMinMax(self, dataFrame, limit=10, save=True, path='', title='', exchangeType='')`

This method takes the `dataFrame` returned by `createDataFrame` method that signifies Slope and Volatility and finds the minimum and maximum symbols (for both volatility and slope) as per the `limit` set. (default 10)
The `save` boolean type determines wether to save the .csv files of minMax and takes a `path` variable if `True`.
`title` and `exchangeType` optional variables are used to title the graphs for better comparison.

It returns a `dict` of `dataframes` : 

```py
minMaxDict = {'min returns' : minRet, 'max returns' : maxRet, 'min volatility' : minVol, 'max volatility' : maxVol}
```

```py
minMax = pe.findMinMax(df, path=pathToSave, title=title, exchangeType=exchangeType)
```


## An example code to Fetch symbols, Fetch data, Create a dataframe, use mongodb to save and fetch data and plot graphs from 2015-2020 yearly with .csv files to store eccentric values and minmax values.

```py
import seaborn as sns
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
import math
from equity_data import FetchData, ProcessData
from datetime import date

plt.style.use('ggplot')

fe = FetchData()
pe = ProcessData()

exchangeType = 'nse'

pathToTicker = 'TickerList/singapore_tickers.csv'
tickers = fe.fetchSymbols('nse')

pathToSave = 'plottings/testLimitsSvg'

randomTickers = tickers.sample(n=50)
normaliser = 'oldest'

duration = {
    '2015-01-01': '2016-01-01', '2016-01-01': '2017-01-01', 
    '2017-01-01': '2018-01-01', '2018-01-01': '2019-01-01', 
    '2019-01-01': '2020-01-01', '2020-01-01': '2020-07-01'
}

for start, end in duration.items():
    print(f'From {start} -> {end} for {tickers.size} symbols')
    df = pe.createDataFrame(randomTickers, limit=100, exchangeType=exchangeType, duration=[start, end], normaliser=normaliser, path=pathToSave)
    title=f'{start}->{end}-{normaliser}PriceMethod'

    minMax = pe.findMinMax(df, path=pathToSave, title=title, exchangeType=exchangeType)

    x = df['slope']
    y = df['volatility']

    plt.figure(figsize=(20, 10))
    plt.axis([-10, 10, -10, 10])

    sns.regplot(x, y,line_kws={'color':'#2E0074', 'label':'Linear Fit'}, marker='o', scatter_kws={'s':40, 'alpha':0.5, 'color':'#74004B'}, label='DataPoints')
    
    slope, intercept = np.polyfit(x, y, 1)
    plt.legend([], f'Slope: {slope}')
    plt.title(f'R/V : {title} | {exchangeType} | Slope = {slope}')
    plt.xlabel('Returns')
    plt.ylabel('Volatility')
    plt.savefig(f'{pathToSave}/{exchangeType} | {title}Scatter.svg', format='svg')
```
