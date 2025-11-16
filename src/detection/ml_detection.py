# src/detection/ml_detection.py
import os
import pandas as pd
from sklearn.ensemble import IsolationForest

# -----------------------
# Paths
# -----------------------
FEATURE_CSV = "data/features/feature_table.csv"
ALERT_DIR = "data/alerts"
ALERT_FILE = os.path.join(ALERT_DIR, "ml_alerts.csv")
os.makedirs(ALERT_DIR, exist_ok=True)

print("[+] Loading feature table...")
df = pd.read_csv(FEATURE_CSV)

# -----------------------
# Select numeric columns for ML
# -----------------------
numeric_cols = ["action_count", "unique_hosts", "suspicious_process_count"]
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
print(f"[✓] ML alerts saved to {ALERT_FILE}")
print(f"[✓] Number of ML alerts: {len(alerts_df)}")
