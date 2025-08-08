#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 19:15:51 2025

@author: adriandominguezcastro
"""

# Get Data from a File using Python


import pandas as pd
import os

def load_data():
    file_path = input("Enter the path or name of your data file (CSV, Excel, or JSON): ").strip()

    if not os.path.exists(file_path):
        print("❌ File not found. Please check the path and try again.")
        return None

    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(file_path)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(file_path)
        elif ext == ".json":
            df = pd.read_json(file_path)
        else:
            print("❌ Unsupported file format.")
            return None

        print("\n✅ Data loaded successfully! First 5 rows:")
        print(df.head())
        return df

    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None


if __name__ == "__main__":
    df = load_data()


