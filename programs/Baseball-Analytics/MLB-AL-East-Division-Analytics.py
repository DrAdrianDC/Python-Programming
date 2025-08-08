#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 17:16:41 2024

@author: adriandominguezcastro
"""


print("Baseball Analytics")
print("using Python with web scraping, data manipulation with pandas and data analysis")


import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.express as px
import base64
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO

# URL of the MLB standings table on Baseball-Reference
url = "https://www.baseball-reference.com/leagues/MLB-standings.shtml"


# Make the GET request
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


# Extract the first table on the page
table = soup.find('table')

# Read the table into a DataFrame
df = pd.read_html(str(table))[0]

# Display the DataFrame
print(df)


# Filter and clean the data
df = df[['Tm', 'W', 'L']]
df.columns = ['Team', 'Wins', 'Losses']


# Manually add URLs of the logos (update these URLs if necessary)
logos = {
    "New York Yankees": "team_logos/New-York-Yankees-tm.png",
    "Boston Red Sox": "team_logos/Boston-Red-Sox-tm.png",
    "Toronto Blue Jays": "team_logos/Toronto-Blue-Jays-tm.png",
    "Tampa Bay Rays": "team_logos/Tampa-Bay-Rays-tm.png",
    "Baltimore Orioles": "team_logos/Baltimore-Orioles-tm.png"
}


df['Logo'] = df['Team'].map(logos)


# Function to encode images in base64
def encode_image(image_path):
    img = Image.open(image_path)
    buffer = BytesIO()
    img.save(buffer, format='png')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

# Add a column with the encoded logos
df['Logo'] = df['Team'].map(lambda x: encode_image(logos[x]) if x in logos else None)



# Create an interactive bar chart with Plotly
fig = px.bar(
    df,
    x="Team",
    y=["Wins", "Losses"],
    title="MLB Team Results",
    text_auto=True,
    labels={"value": "Number of Games", "variable": "Result"}
)

# Add images (logos) to the chart
for i, row in df.iterrows():
    fig.add_layout_image(
        dict(
            source=row['Logo'],
            x=row['Team'],
            y=max(row['Wins'], row['Losses']) + 5,
            xref="x",
            yref="y",
            sizex=0.5,
            sizey=10,
            xanchor="center",
            yanchor="bottom"
        )
    )

# Update the layout to prevent images from overlapping with bar labels
fig.update_layout(
    xaxis_tickangle=-45,
    xaxis_title="Team",
    yaxis_title="Number of Games",
    margin=dict(t=40, b=40, l=40, r=40),
    xaxis=dict(tickmode='array', tickvals=[])  # Remueve los nombres de los equipos del eje x
)

# Display the chart
fig.show()

# Save the chart as an PNG file so it can be viewed with logos
fig.write_image("mlb_team_results.png")



 


