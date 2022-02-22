#Computing the rolling least squares regression of Apple to Microsoft stock movement as:
    #Percent change in the adjusted close price from 2000 to the present
#Pulling data from Yahoo
from pandas_datareader import data as web
import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS
aapl = web.get_data_yahoo('AAPL', '2000-01-01')['Adj Close']
msft = web.get_data_yahoo('MSFT', '2000-01-01')['Adj Close']

#Do we need to drop NAs? Doesn't seem like it for the rolling OLS
aapl_rets = aapl.pct_change()#.dropna()
msft_rets = msft.pct_change()#.dropna()

#compute and plot one-year moving correlation:
#aapl_rets.rolling(250).corr(msft_rets).plot()

#Doesn't capture differences in volatility.
#Rolling least squares regression models dynamic relationship:
model = RollingOLS(endog=aapl_rets, exog=msft_rets, window=250).fit()

model.params.plot(title='One-year beta (OLS regression coefficient of Apple to Microsoft')