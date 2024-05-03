import pandas as pd
import plotly.graph_objects as go
import tkinter as tk
from tkinter.filedialog import askopenfilename
import os

# Initialize Tkinter root
tk.Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

# Show an "Open" dialog box and return the path to the selected file
filename = askopenfilename()

if filename:
    df = pd.read_csv(filename)
    print("File loaded successfully.")

    df['Price'] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    df.dropna(inplace=True) 

    df.index = pd.date_range(start=pd.Timestamp.today().normalize(), periods=len(df), freq='min')

    df_ohlc = df['Price'].resample('5min').ohlc()
    df_ohlc['SMA_10min'] = df_ohlc['close'].rolling(window=2).mean()

    fig = go.Figure(data=[go.Candlestick(x=df_ohlc.index,
                                         open=df_ohlc['open'],
                                         high=df_ohlc['high'],
                                         low=df_ohlc['low'],
                                         close=df_ohlc['close']),
                          go.Scatter(x=df_ohlc.index, y=df_ohlc['SMA_10min'], mode='lines', name='10-min SMA', line=dict(color='blue', width=1.5))])

    fig.update_layout(title='5-Min Candlesticks with 10-Min SMA', xaxis_title='Time', yaxis_title='Price', xaxis_rangeslider_visible=False)

    # Check current working directory
    print("Current Working Directory:", os.getcwd())

    # Save the figure as an HTML file
    fig.write_html('candlestick_chart.html')
    print("The plot has been saved as 'candlestick_chart.html' in the directory:", os.getcwd())
else:
    print("No file selected.")
