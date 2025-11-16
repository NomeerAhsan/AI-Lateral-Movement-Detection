# src/detection/ml_detection.py
import os
import pandas as pd
from sklearn.ensemble import IsolationForest

# -----------------------
# Paths
# -----------------------
FEATURE_DIR = "data/features"
FEATURE_CSV = os.path.join(FEATURE_DIR, "feature_table.csv")
ALERT_DIR = "data/alerts"
ALERT_FILE = os.path.join(ALERT_DIR, "ml_alerts.csv")
os.makedirs(ALERT_DIR, exist_ok=True)

# Auto-detect feature table file (check for backup if main file doesn't have required columns)
print("[+] Loading feature table...")
if os.path.exists(FEATURE_CSV):
    df = pd.read_csv(FEATURE_CSV)
    # Check if it has the new columns
    required_cols = ["num_source_ips", "num_unique_commands", "outside_work_hours"]
    if not all(col in df.columns for col in required_cols):
        # Look for backup file
        import glob
        backup_files = glob.glob(os.path.join(FEATURE_DIR, "feature_table_backup_*.csv"))
        if backup_files:
            # Use most recent backup
            latest_backup = max(backup_files, key=os.path.getmtime)
            print(f"[+] Using backup file: {latest_backup}")
            df = pd.read_csv(latest_backup)
        else:
            print("[!] Warning: Feature table missing new columns, but no backup found")
else:
    # Look for backup file
    import glob
    backup_files = glob.glob(os.path.join(FEATURE_DIR, "feature_table_backup_*.csv"))
    if backup_files:
        latest_backup = max(backup_files, key=os.path.getmtime)
        print(f"[+] Using backup file: {latest_backup}")
        df = pd.read_csv(latest_backup)
    else:
        raise FileNotFoundError(f"Feature table not found: {FEATURE_CSV}")

# -----------------------
# Select numeric columns for ML
# -----------------------
# Base columns (always present)
base_cols = ["action_count", "unique_hosts", "suspicious_process_count"]
# Enhanced columns (may be missing in old feature tables)
enhanced_cols = ["num_source_ips", "num_unique_commands", "outside_work_hours"]

# Use only columns that exist
numeric_cols = [col for col in base_cols + enhanced_cols if col in df.columns]
print(f"[+] Using features: {numeric_cols}")

X = df[numeric_cols].values

print("[+] Training Isolation Forest model...")
model = IsolationForest(contamination=0.15, random_state=42)
labels = model.fit_predict(X)
scores = model.decision_function(X)

df["anomaly_score"] = scores
df["is_anomaly"] = labels

# -----------------------
# Create alerts DataFrame
# -----------------------
anoms = df[df["is_anomaly"] == -1].copy()
if not anoms.empty:
    alerts = []
    for _, r in anoms.iterrows():
        details = {
            "action_count": int(r["action_count"]),
            "unique_hosts": int(r["unique_hosts"]),
            "suspicious_process_count": int(r["suspicious_process_count"]),
            "anomaly_score": float(r["anomaly_score"])
        }
        # Add enhanced features if available
        if "num_source_ips" in r:
            details["num_source_ips"] = int(r["num_source_ips"])
        if "num_unique_commands" in r:
            details["num_unique_commands"] = int(r["num_unique_commands"])
        if "outside_work_hours" in r:
            details["outside_work_hours"] = int(r["outside_work_hours"])
        alerts.append({
            "time_window": r["time_window"],
            "user": r["user"],
            "alert_type": "ML anomaly",
            "details": str(details)
        })
    alerts_df = pd.DataFrame(alerts)
else:
    alerts_df = pd.DataFrame(columns=["time_window", "user", "alert_type", "details"])

# -----------------------
# Save alerts
# -----------------------
alerts_df.to_csv(ALERT_FILE, index=False)
print(f"[OK] ML alerts saved to {ALERT_FILE}")
print(f"[OK] Number of ML alerts: {len(alerts_df)}")
