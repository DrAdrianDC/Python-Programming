#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 16:02:42 2024

@author: adriandominguezcastro
"""

# Calculating the distance between two locations using Haversine formula

# Header
print("*********************************************************")
print("**                                                     **") 
print("**             DISTANCE BETWEEN TWO LOCATIONS          **") 
print("**                                                     **") 
print("**             (HAVERSINE FORMULA)                     **") 
print("**                                                     **") 
print("*********************************************************")




# Import libraries
import numpy as np



# Define constants

# Earth Radius 6371 km

R = 6371




# Get user inputs

latitude_1 = float(input("Enter the value in degrees for the latitude of the first location:"))
latitude_2 = float(input("Enter the value in degrees for the latitude of the second location:"))

longitude_1 = float(input("Enter the value in degrees for the longitude of the first location:"))
longitude_2 = float(input("Enter the value in degrees for the longitude of the second location:"))


# Conversion degrees to radiand

latitude_1 = np.radians(latitude_1)
longitude_1 = np.radians(longitude_1)
latitude_2 = np.radians(latitude_2)
longitude_2 = np.radians(longitude_2)

# Difference between the latitude coordinates

delta_latitude = latitude_2 - latitude_1


# Difference between the latitude coordinates

delta_longitude = longitude_2 - longitude_1



# Haversine Formula

def Haversine (delta_latitude, delta_longitude):
    return 2 * R * np.arcsin(np.sqrt(np.sin((delta_latitude)/2)**2 + np.cos(latitude_1) * np.cos(latitude_2) * np.sin((delta_longitude)/2)**2))




# Output

distance = Haversine(delta_latitude, delta_longitude)

print(f'The distance between the two locations is {distance:.2f} km')
