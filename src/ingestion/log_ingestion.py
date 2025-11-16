import os
import pandas as pd
from glob import glob

# -------------------------------
# Define paths using BASE_PATH
# Without using base path we can get path issues when running from different locations
# -------------------------------
# BASE_PATH = project root folder
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_PATH = os.path.join(BASE_PATH, "data", "raw")
PROCESSED_PATH = os.path.join(BASE_PATH, "data", "processed")
OUTPUT_FILE = os.path.join(PROCESSED_PATH, "clean_logs.csv")

# Make sure processed folder exists
os.makedirs(PROCESSED_PATH, exist_ok=True)

# -------------------------------
# Find all CSV files in raw folder
# -------------------------------
csv_files = glob(os.path.join(RAW_PATH, "*.csv"))

# -------------------------------
# Read and process all CSV files
# -------------------------------
dfs = []

for file in csv_files:
    df = pd.read_csv(file)

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Keep only required columns
    df = df[['timestamp', 'user', 'host', 'event_id', 'process_name', 'command_line', 'source_ip']]

    dfs.append(df)

# Concatenate all dataframes
if dfs:
    all_logs = pd.concat(dfs, ignore_index=True)
else:
    all_logs = pd.DataFrame(columns=['timestamp', 'user', 'host', 'event_id', 'process_name', 'command_line', 'source_ip'])

# Sort by timestamp
all_logs = all_logs.sort_values('timestamp')

# -------------------------------
# Save processed logs
# -------------------------------
all_logs.to_csv(OUTPUT_FILE, index=False)
print(f"Processed logs saved to {OUTPUT_FILE}")
