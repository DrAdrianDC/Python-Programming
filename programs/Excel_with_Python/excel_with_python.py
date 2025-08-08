#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 20:55:39 2025

@author: adriandominguezcastro
"""

# Word Trees using Python

print("*************************************") 
print("**                                 **") 
print("**                                 **") 
print("**     EXCEL with PYTHON           **")
print("**                                 **") 
print("**                                 **") 
print("*************************************") 


import pandas as pd

# sample data
data = {
     'Name': ['John', 'Anna', 'Peter', 'Linda'],
     'Age': [28, 35, 42, 29],
     'City': ['New York', 'Paris', 'London', 'Sydney']
}

# create pandas dataframe
df = pd.DataFrame(data)

# Define file path
file_path = 'example.xlsx'

# write dataframe to excel
df.to_excel(file_path, index = False)

print(" Excel file has been created successfully")

