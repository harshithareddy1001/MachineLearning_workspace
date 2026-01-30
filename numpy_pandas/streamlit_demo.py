import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
import datetime
import time

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="CSV Streamlit Demo 🌟",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Sidebar widgets
# -----------------------------
st.sidebar.header("🛠 Controls")

name = st.sidebar.text_input("Enter your name:")
age = st.sidebar.slider("Select your age:", 0, 100, 25)
hobby = st.sidebar.multiselect(
    "Select your hobbies:",
    ["Reading", "Sports", "Gaming", "Music", "Traveling"]
)
upload_file = st.sidebar.file_uploader("Upload a CSV", type=["csv"])
color = st.sidebar.color_picker("Pick your favorite color", "#00f900")
date = st.sidebar.date_input("Pick a date", datetime.date.today())

# -----------------------------
# Main Title
# -----------------------------
st.title("🎉 Streamlit CSV Demo 🎉")
st.markdown(f"Hello **{name or 'Stranger'}**! You are **{age}** years old. Your favorite color is `{color}`.")

if hobby:
    st.markdown(f"Your hobbies are: {', '.join(hobby)}")

st.markdown(f"Selected date: {date}")

# -----------------------------
# Two-column metrics
# -----------------------------
col1, col2, col3 = st.columns(3)
col1.metric("🔥 Temperature", "25 °C", "+2 °C")
col2.metric("💧 Humidity", "60%", "-5%")
col3.metric("💨 Wind Speed", "15 km/h", "+1 km/h")

# -----------------------------
# Button interactivity
# -----------------------------
if st.button("Click Me! 🖱"):
    st.balloons()
    st.success(f"Yay {name or 'User'}! You clicked the button 🎈")

# -----------------------------
# CSV file upload and display
# -----------------------------
st.subheader("📄 CSV File Upload & Preview")
if upload_file is not None:
    try:
        df = pd.read_csv(upload_file)
        st.success("CSV file loaded successfully! ✅")
        st.dataframe(df.head(10))  # Display first 10 rows

        # -----------------------------
        # Actual vs Expected Temperature Bar Chart
        # -----------------------------
        st.subheader("📊 Actual vs Expected Temperature Bar Chart")
        if {'Actual_Temp', 'Expected_Temp'}.issubset(df.columns):
            fig = px.bar(
                df,
                x=df.index,  # Using row index for x-axis
                y=['Actual_Temp', 'Expected_Temp'],
                barmode='group',  # Grouped bars
                color_discrete_map={
                    'Actual_Temp': 'red',
                    'Expected_Temp': 'blue'
                },
                labels={'value': 'Temperature (°C)', 'index': 'Row'},
                title="Actual vs Expected Temperature"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("CSV must contain 'Actual_Temp' and 'Expected_Temp' columns for this chart.")

        # -----------------------------
        # Optional histogram of first numeric column
        # -----------------------------
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            st.subheader("Histogram of first numeric column")
            fig2, ax = plt.subplots()
            ax.hist(df[numeric_cols[0]], bins=20, color=color, alpha=0.7)
            st.pyplot(fig2)
        
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
else:
    st.info("Upload a CSV file using the sidebar to see it here.")

# -----------------------------
# Map example if CSV has lat/lon
# -----------------------------
if upload_file is not None and {'lat', 'lon'}.issubset(df.columns):
    st.subheader("🗺 Map from CSV")
    st.map(df[['lat', 'lon']])

# -----------------------------
# Media (optional fun)
# -----------------------------
st.subheader("🎬 Media Example")
st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
st.audio("https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav", format="audio/wav")
st.video("https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4")

# -----------------------------
# Expander & progress bar
# -----------------------------
with st.expander("ℹ️ More Info"):
    st.write("This section can hold extra information or instructions.")

st.subheader("⏳ Progress Bar")
progress_bar = st.progress(0)
for i in range(101):
    progress_bar.progress(i)
    time.sleep(0.01)

st.success("Streamlit CSV Demo Completed! 🎉")
