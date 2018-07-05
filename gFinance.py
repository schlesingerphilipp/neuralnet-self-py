from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data

# Dow Jones
#param = {
#    'q': ".DJI", # Stock symbol (ex: "AAPL")
#    'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
#    'x': "INDEXDJX", # Stock exchange symbol on which stock is traded (ex: "NASD")
#    'p': "1Y" # Period (Ex: "1Y" = 1 year)
#}
## get price data (return pandas dataframe)
#df = get_price_data(param)
##print(df)
#param2 = {
#    'q': "FTSE", # Stock symbol (ex: "AAPL")
#    'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
#    'x': "INDEXDJX", # Stock exchange symbol on which stock is traded (ex: "NASD")
#    'p': "1Y" # Period (Ex: "1Y" = 1 year)
#}
#print(df)
def getGdata(id=None, interval_size=86400, stock_exchange_symbol=None, period="1Y"):
    if (not id or not stock_exchange_symbol):
        print("MISSING params")
        return;
    param = {
        'q': id, # Stock symbol (ex: "AAPL")
        'i': interval_size, # Interval size in seconds ("86400" = 1 day intervals)
        'x': stock_exchange_symbol, # Stock exchange symbol on which stock is traded (ex: "NASD")
        'p': period # Period (Ex: "1Y" = 1 year)
    }
    return get_price_data(param)