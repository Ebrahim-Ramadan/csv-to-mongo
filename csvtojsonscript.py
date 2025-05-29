import pandas as pd
import json
import csv

# Read the CSV file
csv_file = "products_1739621393__7122.csv"
df = pd.read_csv(csv_file, quoting=csv.QUOTE_ALL, quotechar='"', escapechar='\\')

# Convert to JSON
json_data = df.to_json("products.json", orient="records", lines=True)

# Optional: Preview the JSON data
with open("products.json", "r") as f:
    print(f.read()[:1000])  # Print first 1000 characters