#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 21:21:00 2024

@author: adriandominguezcastro
"""

print("*******************************************") 
print("**                                       **") 
print("**                                       **") 
print("**        TRAPEZOIDAL RULE               **")
print("**                                       **") 
print("**                                       **") 
print("*******************************************") 

print(" The trapezoidal Rule estimates the integral by dividing the area under the curve into trapezoids, calculating the area of each trapezoid, and summing these areas to obtain the approximation ")

print("------------------------------------------------------------------------------------------") 

import math
import inspect

# Define the function to integrate
def f(x):
    return math.sin(x)

# Define the limits of integration and the number of subintervals
a = 0
b = math.pi
n = 1000


def trapezoid_method(f, a, b, n):
    """
    Approximates the definite integral of a function f from a to b using the trapezoid rule.

    Parameters:
    f (function): The function to integrate.
    a (float): The lower limit of integration.
    b (float): The upper limit of integration.
    n (int): The number of subintervals to use.

    Returns:
    float: The approximate value of the integral.
    """
    # Calculate the width of each subinterval
    h = (b - a) / n
    
    # Calculate the sum of the first and last terms
    integral = 0.5 * (f(a) + f(b))
    
    # Calculate the sum of the middle terms
    for i in range(1, n):
        integral += f(a + i * h)
    
    # Multiply by the width of the subintervals to get the final integral value
    integral *= h
    
    return integral


# Loading the data

print("LOADING THE DATA ***")
print(" ")
print("The function in study is: ")
# Print the source code of the function
print(inspect.getsource(f))
print(" ")
print("The lower limit of integration is:", a)
print(" ")
print("The upper limit of integration is:", b)
print(" ")
print("The number of subintervals", n)
print(" ")
print(" ")
print(" ")
print(" ")
# Calculate the integral
print("CALCULATING THE INTEGRAL ***")
result = trapezoid_method(f, a, b, n)
print(f"The approximate value of the integral is: {result}")


print("------------------------------------------------------------------------------------------") 
print(" ")
print("NOTE: ")
print(" You can modify the f function, and the values of a, b, n to suit your specific needs ")


