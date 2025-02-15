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

## How to Use

1- Clone or download this repository to your local machine.

2- Ensure you have Python installed (version 3.8.3 is used here).

3- Install the required libraries using the commands listed in the "Requirements" section.

4- Run the script using the command:

  ```bash
      python weather_scraper.py
  ```
5- When prompted, input the city and country name. For example:

```bash
Enter City Name: New York
Enter Country Name: USA
 ```

6- The script will then output the current temperature and weather condition, if available. Example output:

```bash
Weather in New York:
Temperature: 15°C
Condition: Clear sky
 ```

## Error Handling

If the city or country name is entered incorrectly or if the data cannot be found, the script will return the following message:

```bash
Please check the city name and try again
 ```


## Limitations

* The script relies on the structure of website used. If the website changes its layout or URL structure, the script may no longer work correctly.
  
* Only works for cities and countries available on the Time and Date weather section.


