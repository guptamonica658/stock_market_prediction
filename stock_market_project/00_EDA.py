import numpy as np
import pandas as pd
import plotly.graph_objects as go

datetime_col = 'date'
num_cols = ['open', 'high', 'low', 'close', 'volume']

def set_dtypes(df):
	df['date'] = df[datetime_col].astype('datetime64[ns]')
	for col in num_cols:
		df[col] = df[col].astype('float')
	return df

df = pd.read_csv('./data/NIFTY 50_day.csv')
df = set_dtypes(df)

# take data only starting 2005
df = df[df['date'] > pd.Timestamp('2004-12-31')]
print(df.head())

fig = go.Figure()
fig.add_trace(go.Scatter(x = df['date'], y = df['open'], mode = 'markers', marker= dict(size=10, color='blue')))
fig.show()
print("Plotly command executed. Check your web browser!")
