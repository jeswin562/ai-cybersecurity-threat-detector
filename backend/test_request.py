import pandas as pd
import requests
import json

# Load the dataset
df = pd.read_csv("CICIDS2017_sample.csv")

# Strip whitespace from column names (important!)
df.columns = df.columns.str.strip()

# Remove the label column if it exists
if "Label" in df.columns:
    df = df.drop(columns=["Label"])

# Get first row as a dictionary
sample_data = df.iloc[0].to_dict()

# Send request
url = "http://127.0.0.1:5000/analyze"
headers = {"Content-Type": "application/json"}
response = requests.post(url, headers=headers, json=sample_data)

# Show result
print("Response:", response.json())


