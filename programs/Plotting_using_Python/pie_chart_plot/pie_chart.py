#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 08:32:32 2024

@author: adriandominguezcastro
"""

# Pie Chart

import pandas as pd
import matplotlib.pyplot as plt

data = {'Categories': ['Category A', 'Category B', 'Category C', 'Category D'],
        'Sizes': [15, 30, 45, 10] }

df = pd.DataFrame(data)
df.set_index('Categories', inplace=True)

ax = df.plot.pie(y='Sizes', autopct='%1.1f%%', startangle=120, legend=False)
ax.set_ylabel('')


plt.title('Pie Chart')
plt.savefig('Pie_Chart.png')
plt.show()
