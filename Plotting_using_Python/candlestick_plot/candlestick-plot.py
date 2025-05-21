#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 21 09:32:32 2025

@author: adriandominguezcastro
"""

# Candlestick plot

import plotly.graph_objects as go
import pandas as pd

# Load the data
df = pd.read_csv('stock_data.csv', delimiter=';')

# Convert Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Create candlestick chart
fig = go.Figure(data=[
    go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )
])

fig.update_layout(
    title='Candlestick Chart',
    xaxis_title='Date',
    yaxis_title='Price',
    xaxis_rangeslider_visible=False
)

fig.show()


# Save to file
fig.write_image('candlestick_plot.png')
