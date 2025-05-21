#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 21 08:02:32 2024

@author: adriandominguezcastro
"""

# Donut Chart

import pandas as pd
import matplotlib.pyplot as plt

# Data
data = {'Categories': ['Category A', 'Category B', 'Category C', 'Category D'],
        'Sizes': [15, 30, 45, 10]}

df = pd.DataFrame(data)
df.set_index('Categories', inplace=True)

# Plot Pie Chart
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(df['Sizes'], labels=df.index, autopct='%1.1f%%',
                                  startangle=120, wedgeprops=dict(width=0.4))  # width controls the donut hole

# Add a circle at the center to make it a donut
centre_circle = plt.Circle((0, 0), 0.80, fc='white')
fig.gca().add_artist(centre_circle)

# Styling
ax.set_ylabel('')
plt.title('Donut Chart')

# Save and show
plt.savefig('Donut_Chart.png')
plt.show()
