
# temperature_converter_streamlit.py

import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session memory
if "conversions" not in st.session_state:
    st.session_state.conversions = []

# Conversion functions
def celsius_to_fahrenheit(c):
    return c * 9/5 + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

# Title
st.title("🌡️ Temperature Converter")

# Input controls
option = st.radio("Select the conversion type:", ["Celsius to Fahrenheit", "Fahrenheit to Celsius"])
value = st.number_input("Introduce the temperature value:")

if st.button("Convert"):
    if option == "Celsius to Fahrenheit":
        result = celsius_to_fahrenheit(value)
        conversion_type = "Celsius to Fahrenheit"
        st.success(f"{value}°C = {result:.2f}°F")
    else:
        result = fahrenheit_to_celsius(value)
        conversion_type = "Fahrenheit to Celsius"
        st.success(f"{value}°F = {result:.2f}°C")

    # Save to session state
    st.session_state.conversions.append({
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Type": conversion_type,
        "Input": value,
        "Output": round(result, 2)
    })

# Show conversion history
if st.session_state.conversions:
    df = pd.DataFrame(st.session_state.conversions)
    st.subheader("📊 Conversion History")
    st.dataframe(df)

    # Download button
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name="temperature_conversions.csv",
        mime="text/csv"
    )
