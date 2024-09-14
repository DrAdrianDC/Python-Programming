# Automated Data Analysis and Reporting

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# Loading the Dataset
def load_dataset():
    dataset_name = input("Please enter the name of the dataset (with extension, e.g., 'data.csv'): ")
    try:
        df = pd.read_csv(dataset_name)
        print(f"Dataset '{dataset_name}' loaded successfully!")
        return df, dataset_name
    except FileNotFoundError:
        print("File not found. Please check the name and try again.")
        return None, None

# Data Cleaning
def clean_data(df):
    report = []
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    report.append("\nBasic Information:\n" + info_str)

    summary_stats = df.describe(include='all')
    report.append("\nSummary Statistics:\n" + str(summary_stats))

    initial_rows = df.shape[0]
    df.drop_duplicates(inplace=True)
    duplicates_removed = initial_rows - df.shape[0]
    report.append(f"\n{duplicates_removed} duplicate rows removed.")

    missing_values = df.isnull().sum()
    report.append("\nMissing Values:\n" + str(missing_values[missing_values > 0]))

    if missing_values.sum() > 0:
        print("\nOptions for handling missing values:")
        print("1. Drop rows with missing values")
        print("2. Fill missing values with mean (for numeric columns)")
        print("3. Fill missing values with mode (for categorical columns)")

        choice = input("Choose an option (1/2/3): ")

        if choice == '1':
            df.dropna(inplace=True)
            report.append("\nRows with missing values have been dropped.")
        elif choice == '2':
            numeric_cols = df.select_dtypes(include=np.number).columns
            for col in numeric_cols:
                df[col].fillna(df[col].mean(), inplace=True)
            report.append("Missing numeric values filled with column means.")
        elif choice == '3':
            categorical_cols = df.select_dtypes(include='object').columns
            for col in categorical_cols:
                df[col].fillna(df[col].mode()[0], inplace=True)
            report.append("Missing categorical values filled with column modes.")
        else:
            report.append("Invalid choice. No changes made to missing values.")
    
    return df, report

# Exploratory Data Analysis (EDA)
def perform_eda(df):
    report = []

    # Correlation matrix
    corr = df.corr()
    report.append("\nCorrelation Matrix (for numeric columns):\n" + str(corr))

    # Plot heatmap
    plt.figure(figsize=(12, 8))
    heatmap = sns.heatmap(corr, annot=True, cmap='coolwarm', annot_kws={"size": 10})
    plt.title('Correlation Matrix Heatmap', fontsize=16)
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png')
    plt.close()

    # Plot histograms for numeric features
    hist_files = []
    for col in df.select_dtypes(include=np.number).columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[col], bins=30, kde=True)
        plt.title(f'Histogram of {col}', fontsize=14)
        plt.xlabel(col, fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.tight_layout()
        hist_file = f'histogram_{col}.png'
        plt.savefig(hist_file)
        plt.close()
        hist_files.append(hist_file)
    
    # Plot count plots for categorical features
    count_files = []
    for col in df.select_dtypes(include='object').columns:
        plt.figure(figsize=(10, 6))
        sns.countplot(y=df[col])
        plt.title(f'Count Plot of {col}', fontsize=14)
        plt.xlabel('Count', fontsize=12)
        plt.ylabel(col, fontsize=12)
        plt.tight_layout()
        count_file = f'countplot_{col}.png'
        plt.savefig(count_file)
        plt.close()
        count_files.append(count_file)

    return report, hist_files, count_files


def save_report_to_txt(report, filename="data_report.txt"):
    with open(filename, 'w') as file:
        for line in report:
            file.write(line + '\n')
    print(f"Report saved to '{filename}'")

def main():
    df, dataset_name = load_dataset()
    if df is not None:
        cleaned_df, cleaning_report = clean_data(df)
        eda_report, hist_files, count_files = perform_eda(cleaned_df)
        
        # Combine cleaning and EDA report
        final_report = cleaning_report + eda_report
        
        # Save cleaned dataset
        cleaned_filename = "cleaned_" + dataset_name
        cleaned_df.to_csv(cleaned_filename, index=False)
        print(f"Cleaned dataset saved as '{cleaned_filename}'")

        # Save the report to a text file
        save_report_to_txt(final_report)

if __name__ == "__main__":
    main()


