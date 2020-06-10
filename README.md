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
