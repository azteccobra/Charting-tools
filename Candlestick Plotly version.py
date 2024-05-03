import pandas as pd
import plotly.graph_objects as go
import tkinter as tk
from tkinter.filedialog import askopenfilename
import os

# Specify the directory where you want to save the HTML file
save_directory = 'C:/Users/yourusername/Documents/MyPlots'

# Create the directory if it does not exist
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Initialize Tkinter root
tk.Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

# Show an "Open" dialog box and return the path to the selected file
filename = askopenfilename()

if filename:
    df = pd.read_csv(filename)
    print("File loaded successfully.")

    # Convert the first column to numeric, coercing errors, and clip values at 5
    df['Price'] = pd.to_numeric(df.iloc[:, 0], errors='coerce').clip(upper=5)
    df.dropna(inplace=True) 

    # Create a datetime index with one minute intervals starting from today
    df.index = pd.date_range(start=pd.Timestamp.today().normalize(), periods=len(df), freq='min')

    # Resample the data to create OHLC data every 5 minutes
    df_ohlc = df['Price'].resample('5min').ohlc()
    df_ohlc['SMA_10min'] = df_ohlc['close'].rolling(window=2).mean()

    fig = go.Figure(data=[go.Candlestick(x=df_ohlc.index,
                                         open=df_ohlc['open'],
                                         high=df_ohlc['high'],
                                         low=df_ohlc['low'],
                                         close=df_ohlc['close']),
                          go.Scatter(x=df_ohlc.index, y=df_ohlc['SMA_10min'], mode='lines', name='10-min SMA', line=dict(color='blue', width=1.5))])

    fig.update_layout(title='5-Min Candlesticks with 10-Min SMA', xaxis_title='Time', yaxis_title='Price', xaxis_rangeslider_visible=False)

    # Construct the full path where the file will be saved
    file_path = os.path.join(save_directory, 'candlestick_chart.html')

    # Save the figure as an HTML file to the specified directory
    fig.write_html(file_path)
    print(f"The plot has been saved as 'candlestick_chart.html' in the directory: {save_directory}")
else:
    print("No file selected.")
