# 1 instalar pytho en windows puede ser desde la tiendae


"""
import pandas_datareader.data as web
import datetime    

start = datetime.datetime(2013, 1, 1)
end = datetime.datetime(2016, 1, 27)
today = datetime.date.today()
#df = web.DataReader("^MXX", 'yahoo', start, end)

df = web.DataReader("^MXX", 'yahoo', today, today)


dates =[]
for x in range(len(df)):
    newdate = str(df.index[x])
    newdate = newdate[0:10]
    dates.append(newdate)

df['dates'] = dates

print(df.head())
print(df.tail())
"""
"""
from pandas_datareader import wb
dat = wb.download(indicator='NY.GDP.PCAP.KD', country=['US', 'CA', 'MX'], start=2005, end=2008)
print(dat)
"""


"""
----
from bs4 import BeautifulSoup
import requests

url="https://news.google.com/topstories?hl=es-419&gl=MX&ceid=MX:es-419"
code=requests.get(url)
soup=BeautifulSoup(code.text,'html5lib')
for title in soup.find_all('a',class_="DY5T1d RZIKme"):
    print(title.text)
"""
import numpy as np
import pandas as pd
#used to grab the stock prices, with yahoo
import pandas_datareader as web
from datetime import datetime
#to visualize the results
import matplotlib.pyplot as plt
import seaborn

#select start date for correlation window as well as list of tickers
start = datetime(2017, 1, 1)
symbols_list = ['AAPL', 'F', 'TWTR', 'FB', 'AAL', 'AMZN', 'GOOGL', 'GE']

#array to store prices
symbols=[]

#pull price using iex for each symbol in list defined above
for ticker in symbols_list: 
    r = web.DataReader(ticker, 'yahoo', start)
    # add a symbol column
    r['Symbol'] = ticker 
    symbols.append(r)

# concatenate into df
df = pd.concat(symbols)
df = df.reset_index()
df = df[['Date', 'Close', 'Symbol']]
df.head()


df_pivot = df.pivot('Date','Symbol','Close').reset_index()
df_pivot.head()

corr_df = df_pivot.corr(method='pearson')
#reset symbol as index (rather than 0-X)
corr_df.head().reset_index()
del corr_df.index.name
corr_df.head(10)


#take the bottom triangle since it repeats itself
mask = np.zeros_like(corr_df)
mask[np.triu_indices_from(mask)] = True

#generate plot
seaborn.heatmap(corr_df, cmap='RdYlGn', vmax=1.0, vmin=-1.0 , mask = mask, linewidths=2.5)
plt.yticks(rotation=0) 
plt.xticks(rotation=90) 
plt.show()
