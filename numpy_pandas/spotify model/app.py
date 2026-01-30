import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="Spotify Cluster Predictor")

st.title("🎶 Spotify Song Type Predictor")

# Load model
kmeans = joblib.load("kmeans_model.pkl")
scaler = joblib.load("scaler.pkl")

# Cluster labels
cluster_names = {
    0: "🔥 High Energy Party",
    1: "😊 Happy / Dance",
    2: "😌 Chill / Sad",
    3: "🎧 Mainstream Mix"
}

st.subheader("Select Song Features")

danceability = st.slider("Danceability", 0.0, 1.0, 0.5)
energy = st.slider("Energy", 0.0, 1.0, 0.5)
valence = st.slider("Valence (Mood)", 0.0, 1.0, 0.5)
tempo = st.slider("Tempo (BPM)", 60, 200, 120)
duration = st.slider("Duration (ms)", 60000, 300000, 180000)
popularity = st.slider("Popularity", 0, 100, 50)

if st.button("🎯 Predict Song Type"):

    user_input = np.array([[
        danceability,
        energy,
        valence,
        tempo,
        duration,
        popularity
    ]])

    # Scale input
    user_scaled = scaler.transform(user_input)

    # Predict cluster
    cluster = kmeans.predict(user_scaled)[0]

    st.success(f"🎵 Predicted Song Type: **{cluster_names.get(cluster, 'Unknown')}**")
