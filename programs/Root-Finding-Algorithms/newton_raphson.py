#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 20:28:05 2024

@author: adriandominguezcastro
"""

# Define the function
def f(x):
    return x**2 - 4

# Define the derivative of the function
def df(x):
    return 2*x


# Define the interval for the Newton-Raphson Method
a, b = 1, 3
tol = 1e-6
max_iter = 100

# Define the initial guess for the Newton-Raphson Method
x0 = 3

print("Newton-Raphson Method")

# Define the  Newton-Raphson Method
def newton_raphson(f, df, x0, tol, max_iter):
    x = x0
    for _ in range(max_iter):
        x_new = x - f(x) / df(x)
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    print("Newton-Raphson method fails to converge.")
    return None



print("Finding root using Newton-Raphson Method:")
root_newton_raphson = newton_raphson(f, df, x0, tol, max_iter)
print(f"Root: {root_newton_raphson}")


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
plot_function(f, [a, b], root_newton_raphson)       
