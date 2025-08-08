#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 16:15:53 2025

@author: adriandominguezcastro
"""

# Clean Data using Python
import pandas as pd
import numpy as np
from fpdf import FPDF  

def analyze_and_clean(df):
    report_lines = []

    report_lines.append("--- Initial Data Check ---")
    report_lines.append("Missing values per column before cleaning:")

    # Missing values
    report_lines.append(str(df.isnull().sum()))

    # Drop duplicates
    original_shape = df.shape
    df = df.drop_duplicates()
    removed_duplicates = original_shape[0] - df.shape[0]
    report_lines.append(f"\n Removed {removed_duplicates} duplicate rows.")

    # Fill missing values
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                report_lines.append(f" Filled missing numeric values in '{col}' with median: {median_val}")
            else:
                df[col] = df[col].fillna("Unknown")
                report_lines.append(f" Filled missing non-numeric values in '{col}' with 'Unknown'")

    df = df.convert_dtypes()
    report_lines.append("\n All missing values handled and types converted.")

    return df, report_lines


def save_clean_data(df, filename="cleaned_data.csv"):
    df.to_csv(filename, index=False)
    print(f"\n Cleaned data saved to: {filename}")


def save_report_pdf(report_lines, pdf_filename="cleaning_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for line in report_lines:
        for subline in line.split("\n"):
            pdf.multi_cell(0, 10, subline)

    pdf.output(pdf_filename)
    print(f" PDF report saved to: {pdf_filename}")


