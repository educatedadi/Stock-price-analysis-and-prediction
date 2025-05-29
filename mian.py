import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMA
import warnings
from statsmodels.tsa.stattools import adfuller

warnings.filterwarnings("ignore")


def fetch_stock_data(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    
    if stock_data.empty:
        raise ValueError(f"Failed to fetch data for {stock_symbol}. Check symbol or internet connection.")

    return stock_data['Close']


stock_symbol = "AAPL"
start_date = "2020-03-19"
end_date = "2025-03-19"

stock_prices = fetch_stock_data(stock_symbol, start_date, end_date)

plt.figure(figsize=(12,6))
plt.plot(stock_prices, label=f"{stock_symbol} Stock Price", color='blue')
plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.title(f"Stock Price of {stock_symbol}\nML Assignment for NIMS University by Aditya Raj | Enroll. no.: 137717")
plt.legend()
plt.show()

def check_stationarity(timeseries):
    result = adfuller(timeseries)
    print("ADF Statistic:", result[0])
    print("p-value:", result[1])
    if result[1] <= 0.05:
        print("The time series is stationary.")
    else:
        print("The time series is not stationary. Differencing may be needed.")

check_stationarity(stock_prices)

p, d, q = 5, 1, 2 
model = ARIMA(stock_prices, order=(p, d, q))
model_fit = model.fit()

print(model_fit.summary())

forecast_steps = 30 
forecast = model_fit.forecast(steps=forecast_steps)

future_dates = pd.date_range(start=stock_prices.index[-1], periods=forecast_steps + 1, freq="B")[1:]

plt.figure(figsize=(12,6))
plt.plot(stock_prices, label="Historical Prices", color='blue')
plt.plot(future_dates, forecast, label="Predicted Prices", linestyle="dashed", color='red')
plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.title(f"{stock_symbol} Stock Price Forecast\nAditya Raj | Enroll. no.: 137717 | Section: D2")
plt.legend()
plt.show()