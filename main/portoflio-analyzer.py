## Configuración inicial de entorno



"""

pip install pycairo

"""
import sys
import pandas as pd
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt

from pandas import Series, DataFrame
from matplotlib import style
from pandas.plotting import scatter_matrix
from pandas import Series, DataFrame

import matplotlib.pyplot as plt

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("report-template.html")



print(sys.prefix)



# "Es el conjunto de emisoras que se van a analizar. Puede ser los componentes de un índice o bien de las emisoras participantes en reto actinver.

stocks_watchlist = pd.read_csv('stocks-watchlist.csv')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also\n",
    print(stocks_watchlist)


# Visualizar los datos de una emisora por su símbolo:

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime.now()


df = web.DataReader("GOOGL.MX", 'yahoo', start, end)['Close']



df.plot()
plt.savefig('my_plot.png')








# Mostrar los acumulado de una acción como en investing.com:
tickers = stocks_watchlist['Symbol'].tolist()
df_list = pd.DataFrame()



for ticker in tickers:
    print("Getting data of " + ticker)
    prices = web.DataReader(ticker, 'yahoo', datetime.date.today().year - 1)['Close']

    # get all timestamps for specific lookups
    today = prices.index[-1]
    yesterday= prices.index[-2]
    start_date = prices.index[0]
    weekago_day = prices.index[-8]
    monthago_day = prices.index[-31]
    start_week_day = today - pd.tseries.offsets.Week(weekday=0)
    start_month_day = today - pd.tseries.offsets.BMonthBegin()

    
    # calculate percentage changes
    close = prices[today]
    daily =  ((close - prices[yesterday]) / prices[yesterday] ) * 100
    wtd = ((close - prices[weekago_day]) / prices[weekago_day] )  * 100
    mtd = ((close - prices[monthago_day]) / prices[monthago_day] ) * 100
    ytd = ((close - prices[start_date]) / prices[start_date] )  * 100    
     
    # Create temporary frame for current ticker
    df = pd.DataFrame(data=[[ticker, close, daily, wtd, mtd,  ytd]], columns=['Symbol', 'Close', 'Daily', '1 Week', '1 Month', '1 Year'] )
    df_list = df_list.append(df,ignore_index = True)

    # Stack all frames
    #print(prices[yesterday])
    #print(prices[today])
    #pd.concat(df_list)

df_list.sort_values(by=['1 Year'])
print(df_list)




template_vars = {"title" : "Stocks",
                 "all_stocks_table": stocks_watchlist.to_html(), "stocks_performance" : df_list.to_html()}

html_out = template.render(template_vars)

#write html to file
text_file = open("index.html", "w")
text_file.write(html_out)
text_file.close()