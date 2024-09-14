# Automated Data Analysis and Reporting


This Python script automates the process of loading a dataset, cleaning the data, performing Exploratory Data Analysis (EDA), and generating reports with visualizations. It is designed to provide quick insights into any dataset by handling common tasks such as missing values, duplicate removal, and visualization.

### Features

   - **Load Dataset:** Automatically prompts the user to input the dataset file name.
   - **Data Cleaning:**
        - Removes duplicate rows.
        - Identifies and handles missing values with user-specified options:
            - Drop rows with missing values.
            - Fill missing numeric values with the column mean.
            - Fill missing categorical values with the most frequent value (mode).
   - **Exploratory Data Analysis (EDA):**
        - Generates a correlation matrix and visualizes it with a heatmap.
        - Creates histograms for numeric columns.
        - Generates count plots for categorical columns.
   - **Reporting:**
        - Saves a detailed report of the data cleaning and EDA steps to a text file (data_report.txt).
        - Saves the cleaned dataset as a CSV file (cleaned_<dataset_name>.csv).
        - Generates and saves plots as PNG files.

### Requirements

 **Python 3.8.3**
 
Required libraries:

 **pandas**
 **numpy**
 **matplotlib**
 **seaborn**
