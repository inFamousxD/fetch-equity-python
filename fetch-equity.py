from alpha_vantage.timeseries import TimeSeries 
from datetime import date

def stockchart(symbol):
    ts = TimeSeries(key='A0S8E16C6LW13EVL', output_format='pandas')
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')

    years = 2
    dt = date.today()
    dt = dt.replace(year=dt.year-years)
    today = date.today()
    print(f'Printing data from {dt} up until {today}')
    print()

    data_concat = data[:dt]
    print(data_concat)


# symbol=input("Enter symbol name:") 
stockchart('NSE:COFFEEDAY')