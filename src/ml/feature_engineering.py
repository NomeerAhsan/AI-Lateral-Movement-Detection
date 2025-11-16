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

# ---- Feature 4: Number of unique source IPs per window ----
unique_source_ips = (
    df.groupby(['user', 'time_window'])['source_ip']
      .nunique()
      .reset_index(name="num_source_ips")
)

# ---- Feature 5: Number of unique commands per window ----
# Filter out rows where command_line is missing or just "-"
df_commands = df[df['command_line'].notna() & (df['command_line'] != '-')].copy()
unique_commands = (
    df_commands.groupby(['user', 'time_window'])['command_line']
      .nunique()
      .reset_index(name="num_unique_commands")
)

# ---- Feature 6: Outside work hours indicator ----
# Define work hours as 06:00-18:00, so outside is 00:00-06:00 or 18:00-23:59
df['hour'] = df['timestamp'].dt.hour
df['outside_work_hours'] = ((df['hour'] >= 0) & (df['hour'] < 6)) | (df['hour'] >= 18)
outside_work_hours = (
    df.groupby(['user', 'time_window'])['outside_work_hours']
      .any()  # True if any activity in window is outside work hours
      .astype(int)
      .reset_index(name="outside_work_hours")
)

# ---- Combine all features ----
feature_table = action_counts.merge(unique_hosts, on=['user', 'time_window'])
feature_table = feature_table.merge(suspicious_counts, on=['user', 'time_window'])
feature_table = feature_table.merge(unique_source_ips, on=['user', 'time_window'], how='left')
feature_table = feature_table.merge(unique_commands, on=['user', 'time_window'], how='left')
feature_table = feature_table.merge(outside_work_hours, on=['user', 'time_window'], how='left')

# Fill NaN values (for windows with no commands or source IPs)
feature_table['num_source_ips'] = feature_table['num_source_ips'].fillna(0).astype(int)
feature_table['num_unique_commands'] = feature_table['num_unique_commands'].fillna(0).astype(int)
feature_table['outside_work_hours'] = feature_table['outside_work_hours'].fillna(0).astype(int)

print("[+] Saving feature table to:", OUTPUT_CSV)

# Try to save, with error handling for locked files
try:
    feature_table.to_csv(OUTPUT_CSV, index=False)
    print("[OK] Feature engineering complete!")
    print("[OK] Output generated at data/features/feature_table.csv")
except (PermissionError, OSError) as e:
    # If file is locked, write to a backup file
    import datetime
    backup_file = OUTPUT_CSV.replace('.csv', f'_backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    try:
        feature_table.to_csv(backup_file, index=False)
        print(f"[!] Warning: Could not write to {OUTPUT_CSV} (file may be open in another program)")
        print(f"[OK] Feature table saved to backup file: {backup_file}")
        print("[!] Please close the file and run again, or use the backup file")
    except Exception as e2:
        print(f"[ERROR] Could not save feature table: {e2}")
        raise
