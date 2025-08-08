#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 09:11:03 2024

@author: adriandominguezcastro
"""

import matplotlib.pyplot as plt

# Data for plotting
x = [0, 1, 2, 3, 4, 5]
y = [0, 1, 4, 9, 16, 25]

# Create a figure and axis
plt.figure(figsize=(8,6))

# Plotting the line
plt.plot(x, y, label='y = x^2', color='blue', marker='o')

# Adding labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Simple Line Plot')

# Add grid and legend
plt.grid(True)
plt.legend()

# Save plot
plt.savefig('Plot.png')

# Show plot
plt.show()
