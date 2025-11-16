# AI-Lateral-Movement-Detection

AI-powered lateral movement detection system for early threat detection using both rule-based and machine learning approaches.

## Overview

This project implements a comprehensive lateral movement detection system that:
- Ingests and normalizes security logs
- Extracts behavioral features from user activity
- Detects anomalies using both rule-based and ML-based methods
- Merges and visualizes alerts for security analysis

## Project Structure

```
AI-Lateral-Movement-Detection/
├── data/
│   ├── raw/                    # Raw synthetic logs
│   ├── processed/              # Cleaned and normalized logs
│   ├── features/               # Feature engineering output
│   └── alerts/                 # Detection alerts
│       └── visualizations/     # Generated charts and graphs
├── src/
│   ├── ingestion/              # Log ingestion scripts
│   ├── ml/                     # Feature engineering
│   ├── detection/              # Detection algorithms
│   │   ├── rule_based_detection.py
│   │   ├── ml_detection.py
│   │   └── merge_alerts.py
│   └── utils/                  # Utility scripts
│       └── visualize_alerts.py
├── notebooks/                  # Jupyter notebooks (optional)
├── docs/                       # Project documentation
├── tests/                      # Unit tests
├── run_pipeline.py             # End-to-end pipeline script
└── requirements.txt            # Python dependencies
```

## Features

### Detection Methods

1. **Rule-Based Detection** (`rule_based_detection.py`)
   - Multiple hosts accessed in short time (10 minutes)
   - Login outside working hours (00:00-06:00)
   - Remote process creation (powershell.exe, cmd.exe)
   - Sensitive host access by uncommon users

2. **ML-Based Detection** (`ml_detection.py`)
   - Uses Isolation Forest algorithm
   - Detects anomalies based on behavioral patterns
   - Enhanced with 6 features for better detection

### Feature Engineering

The system extracts the following features per user per 10-minute time window:

1. **action_count**: Total number of actions/events
2. **unique_hosts**: Number of unique hosts accessed
3. **suspicious_process_count**: Count of suspicious processes executed
4. **num_source_ips**: Number of unique source IPs
5. **num_unique_commands**: Number of unique commands executed
6. **outside_work_hours**: Binary indicator (1 if activity outside 06:00-18:00)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AI-Lateral-Movement-Detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- pandas
- numpy
- scikit-learn
- matplotlib
- networkx (for future graph-based features)

## Usage

### Quick Start - Run Complete Pipeline

Run the end-to-end pipeline:
```bash
python run_pipeline.py
```

This will execute:
1. Feature Engineering
2. ML Detection
3. Rule-Based Detection (if not already done)
4. Merge Alerts

### Step-by-Step Execution

#### 1. Log Ingestion
```bash
python src/ingestion/log_ingestion.py
```
- Input: `data/raw/synthetic_logs.csv`
- Output: `data/processed/clean_logs.csv`
- Normalizes timestamps and extracts relevant fields

#### 2. Feature Engineering
```bash
python src/ml/feature_engineering.py
```
- Input: `data/processed/clean_logs.csv`
- Output: `data/features/feature_table.csv`
- Generates 6 features per user per 10-minute window

#### 3. ML Detection
```bash
python src/detection/ml_detection.py
```
- Input: `data/features/feature_table.csv`
- Output: `data/alerts/ml_alerts.csv`
- Trains Isolation Forest and generates anomaly alerts

#### 4. Rule-Based Detection
```bash
python src/detection/rule_based_detection.py
```
- Input: `data/processed/clean_logs.csv`
- Output: `data/alerts/alerts.csv`
- Applies hard-coded rules for known attack patterns

#### 5. Merge Alerts
```bash
python src/detection/merge_alerts.py
```
- Input: `data/alerts/ml_alerts.csv` + `data/alerts/alerts.csv`
- Output: `data/alerts/all_alerts.csv`
- Combines and sorts all alerts by time window

#### 6. Visualize Alerts
```bash
python src/utils/visualize_alerts.py
```
- Input: `data/alerts/all_alerts.csv`
- Output: `data/alerts/visualizations/*.png`
- Generates 6 visualization charts:
  - Alerts per user
  - Alerts per host
  - Alerts over time
  - Alert type distribution
  - ML vs Rule-based comparison
  - User activity timeline

## Output Files

### Data Files
- `data/processed/clean_logs.csv`: Normalized log data
- `data/features/feature_table.csv`: Engineered features
- `data/alerts/ml_alerts.csv`: ML-based anomaly alerts
- `data/alerts/alerts.csv`: Rule-based alerts
- `data/alerts/all_alerts.csv`: Merged alerts (sorted by time)

### Visualizations
All charts are saved in `data/alerts/visualizations/`:
- `alerts_per_user.png`
- `alerts_per_host.png`
- `alerts_over_time.png`
- `alert_type_distribution.png`
- `ml_vs_rule_based.png`
- `user_activity_timeline.png`

## Detection Rules

### Rule-Based Detection

1. **Multiple Hosts in Short Time**
   - Triggers when a user accesses different hosts within 10 minutes
   - Indicates potential lateral movement

2. **Login Outside Working Hours**
   - Detects logins between 00:00-06:00
   - Unusual activity pattern

3. **Remote Process Creation**
   - Flags execution of suspicious processes:
     - powershell.exe
     - cmd.exe
   - Common in lateral movement attacks

4. **Sensitive Host Access**
   - Detects access to sensitive hosts by unauthorized users
   - Example: Finance user accessing HR servers

### ML-Based Detection

- Uses **Isolation Forest** algorithm
- Contamination rate: 15% (configurable)
- Detects anomalies based on:
  - Unusual action patterns
  - Abnormal host access patterns
  - Suspicious process execution frequency
  - Multiple source IPs
  - Command diversity
  - Off-hours activity

## Example Output

```
Total Alerts: 6

By User:
ali     3
sara    3

By Alert Type:
Remote process creation         3
Multiple hosts in short time    2
ML anomaly                      1

By Detection Method:
Rule-based    5
ML            1
```

## Configuration

### ML Model Parameters
Edit `src/detection/ml_detection.py`:
- `contamination=0.15`: Expected proportion of anomalies
- `random_state=42`: For reproducibility

### Time Window
Edit `src/ml/feature_engineering.py`:
- Default: 10-minute windows (`dt.floor("10min")`)
- Adjust based on your log volume and analysis needs

### Work Hours
Edit `src/ml/feature_engineering.py`:
- Default: 06:00-18:00
- Outside hours: 00:00-06:00 and 18:00-23:59

## Future Enhancements

- [ ] Graph-based detection using networkx
- [ ] Real-time log streaming
- [ ] Alert prioritization and scoring
- [ ] Integration with SIEM systems
- [ ] User behavior profiling
- [ ] Automated response actions
- [ ] Model retraining pipeline
- [ ] Performance metrics dashboard

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license here]

## Acknowledgments

- Isolation Forest algorithm from scikit-learn
- Synthetic log generation for testing

## Contact

[Add contact information]

---

**Note**: This system currently uses synthetic logs for development and testing. Replace with real log data for production use.
