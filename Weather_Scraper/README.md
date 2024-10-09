# Weather Scraper


## Overview

This Python script allows users to get the current weather data for any city by scraping the weather information from the Time and Date website (https://www.timeanddate.com/). It takes the city and country as input, constructs the URL based on these inputs, and then retrieves the current temperature and weather condition of the specified city.

## Features

  - Takes the city and country name as user input.
  - Retrieves and displays the current temperature and weather condition of the specified city.
  - Gracefully handles incorrect city names by prompting the user to try again.

## Requirements

- Python 3.8.3

The script uses the following Python libraries:

    requests: To make HTTP requests to the Time and Date website.
    BeautifulSoup (from bs4): To parse and extract weather data from the HTML of the webpage.

You can install the required libraries using the following commands:

```bash
pip install requests
pip install beautifulsoup4
```


