import pandas as pd
import os

# Correct paths based on your project structure
INPUT_CSV = "data/processed/clean_logs.csv"
OUTPUT_CSV = "data/features/feature_table.csv"

# Ensure output folder exists
os.makedirs("data/features", exist_ok=True)

print("[+] Loading cleaned logs...")

df = pd.read_csv(INPUT_CSV)

# Convert timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])

print("[+] Generating features...")

# ---- Feature 1: Actions per user per 10-minute window ----
df['time_window'] = df['timestamp'].dt.floor("10min")
action_counts = (
    df.groupby(['user', 'time_window'])
      .size()
      .reset_index(name='action_count')
)

# ---- Feature 2: Number of unique hosts touched per window ----
unique_hosts = (
    df.groupby(['user', 'time_window'])['host']
      .nunique()
      .reset_index(name="unique_hosts")
)

# ---- Feature 3: Suspicious process execution count ----
df['is_suspicious_process'] = df['process_name'].isin([
    "powershell.exe", "cmd.exe", "wmic.exe", "psexec.exe"
]).astype(int)

suspicious_counts = (
    df.groupby(['user', 'time_window'])['is_suspicious_process']
      .sum()
      .reset_index(name="suspicious_process_count")
)

# ---- Combine all features ----
feature_table = action_counts.merge(unique_hosts, on=['user', 'time_window'])
feature_table = feature_table.merge(suspicious_counts, on=['user', 'time_window'])

print("[+] Saving feature table to:", OUTPUT_CSV)

feature_table.to_csv(OUTPUT_CSV, index=False)

print("[✓] Feature engineering complete!")
print("[✓] Output generated at data/features/feature_table.csv")
