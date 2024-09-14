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

You can install the dependencies by running: 
```bash
pip install pandas numpy matplotlib seaborn 
```

### How to Use
1- Clone this repository or download the script.
2- Place your dataset (CSV file) in the same directory as the script.
3- Run the script using a Python environment:
```bash
python <script_name>.py
```
4- You will be prompted to input the dataset name (with extension), for example:
```bash
Please enter the name of the dataset (with extension, e.g., 'data.csv'): my_data.csv
```

5- Follow the on-screen instructions for handling missing values:

    - Option 1: Drop rows with missing values.
    - Option 2: Fill missing numeric values with the column mean.
    - Option 3: Fill missing categorical values with the most frequent value.

6- After execution, the following outputs will be generated:

    - Cleaned Dataset: Saved as cleaned_<dataset_name>.csv.
    - Data Report: A text file named data_report.txt, containing:
       - Basic information about the dataset.
       - Summary statistics.
       - Details of duplicate removal and missing value handling.
       - Correlation matrix.
    - Plots: Correlation heatmap, histograms, and count plots saved as PNG files.




