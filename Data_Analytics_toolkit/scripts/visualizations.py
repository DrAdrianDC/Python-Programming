#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 11:15:51 2025

@author: adriandominguezcastro
"""

# Data Visualizations

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_summary(df):
    st.write("### 📋 Summary Statistics")
    st.dataframe(df.describe())

    # 1. Missing Values Bar Chart
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        st.write("### 🧩 Missing Values")
        fig, ax = plt.subplots(figsize=(10, 4))
        missing.sort_values(ascending=False).plot(kind='bar', color='salmon', ax=ax)
        ax.set_ylabel("Missing Count")
        st.pyplot(fig)
    else:
        st.success("No missing values found!")

    # 2. Correlation Heatmap
    numeric_cols = df.select_dtypes(include='number')
    if numeric_cols.shape[1] > 1:
        st.write("### 🔗 Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
    else:
        st.info("Not enough numeric features for a correlation heatmap.")

    # 3. Optional: Pairplot for small datasets
    if 2 <= numeric_cols.shape[1] <= 5 and df.shape[0] <= 500:
        st.write("### 🔍 Pairplot (Sample)")
        fig = sns.pairplot(numeric_cols.sample(min(len(df), 200)))
        st.pyplot(fig)

    # 4. Histograms
    st.write("### 📊 Feature Distributions")
    for col in numeric_cols.columns:
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax, color='skyblue')
        ax.set_title(f"Distribution of {col}")
        st.pyplot(fig)
