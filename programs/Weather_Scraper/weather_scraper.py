#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 18:44:12 2024

@author: adriandominguezcastro
"""

# Weather in City, Country

# pip install beautifulsoup4


import requests
from bs4 import BeautifulSoup



# Get city and country input from user
city = input("Enter City Name: ")
country = input("Enter Country Name: ")

city_formatted = city.lower().replace(" ", "-")
country_formatted = country.lower().replace(" ", "-")

# Construct the URL with the country and city
url = f"https://www.timeanddate.com/weather/{country_formatted}/{city_formatted}"
response = requests.get(url)

# Parse the page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

try:
    # Scrape the temperature
    temperature = soup.find("div", class_="h2").get_text(strip=True)
    
    # Scrape the weather condition/description (if available)
    description = soup.find("div", class_="h2").find_next("p").get_text(strip=True)

    

    # Output the results
    print(f"Weather in {city}:")
    print(f"Temperature: {temperature}")
    print(f"Condition: {description}")

except AttributeError:
    print("Please check the city name and try again")
    


    
