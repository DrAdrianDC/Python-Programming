#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:16:51 2025

@author: adriandominguezcastro
"""

# Data Analytics Toolkit


import streamlit as st
import pandas as pd
import os

from scripts.get_data import load_data
from scripts.clean_data import analyze_and_clean, save_clean_data, save_report_pdf
from scripts.eda import generate_report
from scripts.visualizations import plot_summary

st.title("Data Analytics Toolkit")

#st.write("A Python-based automated pipeline to streamline data collection, cleaning, exploratory analysis, visualization, and results export")

# Include a PNG image
st.image("word-tree-figure.png", caption="Data Analytics Toolkit", width=500)

st.write(" ")  
st.write("  \n")

uploaded_file = st.file_uploader("Upload your CSV, Excel, or JSON file", type=["csv", "xlsx", "xls", "json"])

if uploaded_file:
    ext = uploaded_file.name.split('.')[-1].lower()
    
    if ext == "csv":
        df = pd.read_csv(uploaded_file)
    elif ext in ["xlsx", "xls"]:
        df = pd.read_excel(uploaded_file)
    elif ext == "json":
        df = pd.read_json(uploaded_file)
    else:
        st.error("Unsupported file format")
        df = None

    if df is not None:
        st.subheader("📄 Raw Data")
        st.write(df.head())

        if st.button("🧼 Clean Data"):
            #df_clean = analyze_and_clean(df)
            df_clean, report_lines = analyze_and_clean(df)
            st.subheader("✅ Cleaned Data")
            st.write(df_clean.head())

            # Save cleaned dataset
            save_clean_data(df_clean)

            # Save PDF report for cleaning data
            save_report_pdf(report_lines)

            # Mostrar el informe en pantalla (opcional)
            st.subheader("📝 Cleaning Report Summary")
            st.text("\n".join(report_lines))

            # Descargar el PDF
            with open("cleaning_report.pdf", "rb") as pdf_file:
                st.download_button(
                    label="📄 Download Cleaning Report (PDF)",
                    data=pdf_file,
                    file_name="cleaning_report.pdf",
                    mime="application/pdf"
               )

    st.subheader("Select Exploratory Data Analysis type:")
    eda_option = st.radio("Choose analysis type:", ["Sweetviz Report", "Interactive Visualizations"])

    if eda_option == "Sweetviz Report":
        output_path = generate_report(df)
        st.write("Output path:", output_path)

        if output_path and os.path.exists(output_path):
            # Leer y mostrar el HTML en Streamlit
            with open(output_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=1000, scrolling=True)

            # Botón para descargar el HTML
            with open(output_path, 'rb') as f:
                st.download_button(
                    label="⬇️ Download EDA Report (HTML)",
                    data=f,
                    file_name="eda_report.html",
                    mime="text/html"
                )
        else:
            st.error("❌ Could not generate the Sweetviz report. Please check your dataset.")

    elif eda_option == "Interactive Visualizations":
        plot_summary(df)

   