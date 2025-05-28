# frontend/app.py

import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="AI Threat Detector", layout="wide")
st.title("🔐 AI Cybersecurity Threat Detector")

st.markdown("""
Upload a CSV file containing network traffic data.  
The app will analyze each row using your trained model and return predictions:
- ✅ **Normal**
- 🚨 **Malicious**
""")

uploaded_file = st.file_uploader("📁 Upload CSV File", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()  # Clean column names
    st.write("📄 **Uploaded Data Preview:**")
    st.dataframe(df.head())

    if st.button("🚀 Analyze"):
        st.markdown("### 🔎 Results")
        results = []
        for index, row in df.iterrows():
            # Send each row to your Flask API
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/analyze",
                    json=row.to_dict(),
                    headers={"Content-Type": "application/json"}
                )
                prediction = response.json().get("prediction", "Error")
            except:
                prediction = "Error contacting API"

            results.append(prediction)

        df["Prediction"] = results
        st.success("✅ Analysis Complete")
        st.dataframe(df)

        # Optional: download result
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Results", csv, "prediction_results.csv", "text/csv")


import plotly.express as px

# Count predictions
prediction_counts = df["Prediction"].value_counts().to_dict()
labels = list(prediction_counts.keys())
values = list(prediction_counts.values())

# Show pie chart
st.markdown("### 📊 Prediction Summary")
fig = px.pie(names=labels, values=values, title="Prediction Breakdown")
st.plotly_chart(fig)

# Visual alert
malicious_ratio = prediction_counts.get("Malicious", 0) / len(df)
if malicious_ratio > 0.3:
    st.error(f"⚠️ High Threat Level Detected: {malicious_ratio:.0%} of traffic is malicious!")
else:
    st.success("✅ Low Threat Level")

st.markdown("""
---
Developed by **Jeswin**  
🔗 [GitHub](https://github.com/jeswin562)
""")


