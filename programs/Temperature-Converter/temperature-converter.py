#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 22:07:25 2024

@author: adriandominguezcastro
"""

# Title of the program
title = "TEMPERATURE CONVERTER"
print(title)

# Display conversion options
print("1. Celsius to Fahrenheit ")
print("2. Fahrenheit to Celsius")

# Get the user's selection
select = input("Select an option: ")

# Check if the selection is valid
if select != "1" and select != "2":
    print("Invalid option")
else:
    # Get the temperature to convert
    degrees = float(input("Temperature: "))



    # Perform the conversion based on the selection
    if select == "1":
       fahrenheit = (degrees * 9/5) + 32
       print("The temperature on the Fahrenheit scale is ", fahrenheit)
    elif select == "2":
       celsius = (degrees - 32) * 5/9
       print("The temperature on Celsius scale is", celsius)


    

