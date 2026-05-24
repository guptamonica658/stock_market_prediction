import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy import stats

datetime_col = 'date'
num_cols = ['open', 'high', 'low', 'close', 'volume']
start_date = pd.Timestamp('2004-12-31')
end_date  = pd.Timestamp('2025-12-31')

def set_dtypes(df):
	df['date'] = df[datetime_col].astype('datetime64[ns]')
	for col in num_cols:
		df[col] = df[col].astype('float')
	return df

df = pd.read_csv('../data/NIFTY 50_day.csv')
df = set_dtypes(df)

# take data only starting 2005
df = df[(df['date'] > start_date) & (df['date'] < end_date)]
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
#target
df['log_return'] = np.log(df['close'].shift(-1)/df['close'])
print(df.head())
print(df.tail())

# raw columns EDA
#check if all data is correct

if not (df[df["high"]<df["open"]].empty):
	print(f'wrong data where high is less than open')
if not (df[df["high"]<df["close"]].empty):
	print(f'wrong data where high is less than close')
if not (df[df["low"]>df["open"]].empty):
	print(f'wrong data where low is less than open')
if not (df[df["low"]>df["close"]].empty):
	print(f'wrong data where low is less than close')
else:
	print("no issues with the data")

# fig = go.Figure()
# fig.add_trace(go.Scatter(x = df['date'], y = df['open'], mode = 'markers', marker= dict(size=10, color='blue')))
# fig.show()

# Distribution plot
fig = plt.subplots(figsize = (10,10))
plt.hist(df['open'], bins = 30, alpha = 0.5, label = 'opening price', color = 'blue', edgecolor='black', density = True)
plt.hist(df['close'], bins = 30, alpha = 0.5, label = 'closing price', color = 'green', edgecolor='black', density = True)
plt.hist(df['high'], bins = 30, alpha = 0.5, label = 'daily high', color = 'orange', edgecolor='black', density = True)
plt.hist(df['low'], bins = 30, alpha = 0.5, label = 'daily low', color = 'red', edgecolor='black', density = True)
plt.title("Daily data")
plt.xlabel('Values')
plt.ylabel('Frequency')
plt.legend()
plt.show()

## QQ plot
stats.probplot(df['open'], dist = "norm", plot = plt)
plt.title("QQ plot: S shaped curve: data has heavy tails")
plt.show()

# rolling mean and std of "Close"
df["rollingmean_close"] = df['close'].rolling(window=5).mean()
df["rollingstd_close"] = df['close'].rolling(window=5).std()
fig = plt.plot()
plt.scatter(df[datetime_col], df['rollingmean_close'], label = "rolling mean")
plt.scatter(df[datetime_col], df['rollingstd_close'], label='rolling std')
plt.show()

print("Plotly command executed. Check your web browser!")
