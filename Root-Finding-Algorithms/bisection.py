#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 20:27:36 2024

@author: adriandominguezcastro
"""

print("Bisection Method")


# Define the function
def f(x):
    return x**2 - 4

# Define the interval for the Bisection Method
a, b = 1, 3
tol = 1e-6
max_iter = 100

# Define the  Bisection Method
def bisection(f, a, b, tol, max_iter):
    if f(a) * f(b) >= 0:
        print("Bisection method fails.")
        return None
    while (b - a) / 2.0 > tol:
        midpoint = (a + b) / 2.0
        if f(midpoint) == 0:
            return midpoint
        elif f(a) * f(midpoint) < 0:
            b = midpoint
        else:
            a = midpoint
    return (a + b) / 2.0


print("Finding root using Bisection Method:")
root_bisection = bisection(f, a, b, tol, max_iter)
print(f"Root: {root_bisection}")


# Plotting
import matplotlib.pyplot as plt
import numpy as np

def plot_function(f, x_range, root=None):
    x = np.linspace(x_range[0], x_range[1], 400)
    y = f(x)
    plt.plot(x, y, label="f(x)")
    if root is not None:
        plt.axvline(root, color='r', linestyle='--', label=f'Root: {root}')
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.legend()
    plt.show()
    
# Call the plot_function to display the plot
plot_function(f, [a, b], root_bisection)    