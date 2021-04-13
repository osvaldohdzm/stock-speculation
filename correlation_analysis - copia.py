import pandas as pd
import datetime
import pandas_datareader.data as web
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from matplotlib import style
from pandas.plotting import scatter_matrix

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime.now()


dfcomp = web.DataReader(['AAPL', 'GE','FB', 'GOOG', 'IBM', 'MSFT','TSLA'],'yahoo',
                               start=start, 
                               end=end)['Adj Close']
dfcomp.tail()
dfcomp.shape

retscomp = dfcomp.pct_change()

corr = retscomp.corr()



plt.scatter(retscomp.AAPL, retscomp.GE)
plt.xlabel('Returns AAPL')
plt.ylabel('Returns GE')

scatter_matrix(retscomp, diagonal='kde', figsize=(10, 10))

plt.imshow(corr, cmap='hot', interpolation='none')
plt.colorbar()
plt.xticks(range(len(corr)), corr.columns)
plt.yticks(range(len(corr)), corr.columns)
