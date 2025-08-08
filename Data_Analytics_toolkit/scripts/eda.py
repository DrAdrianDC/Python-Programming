#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 09:05:51 2025

@author: adriandominguezcastro
"""

# Exploratory Data Analysis


import matplotlib
matplotlib.use('Agg')
import sweetviz as sv
import os

def generate_report(df, output_file="eda_report.html"):
    try:
        if df is None or df.empty:
            print("[Sweetviz] ❌ DataFrame is empty or None.")
            return None

        # Reintentar generación
        report = sv.analyze(df)
        report.show_html(output_file)

        if os.path.exists(output_file):
            print(f"[Sweetviz] ✅ Report generated: {output_file}")
            return output_file
        else:
            print("[Sweetviz] ❌ HTML file was not created.")
            return None

    except Exception as e:
        print(f"[Sweetviz Error] {e}")
        return None

