# AI-Lateral-Movement-Detection

AI-powered lateral movement detection system for early threat detection

Phase 0: Step 1 — Understanding Log Ingestion

Log ingestion is the process of collecting, normalizing, and storing logs from different systems so they can be analyzed.

Sources:
⦁ Windows Event Logs (4624: login success, 4625: login failure, 4688: process created, etc.)
⦁ Sysmon (process creation, network connections)
⦁ Linux authentication logs (SSH, sudo)
⦁ Network devices / NetFlow / Zeek
⦁ EDR agents (endpoint telemetry)
⦁ Active Directory metadata (users, groups, lastLogonTime)

Using fake logs for training the model then once its completed we will use real logs.

Python Log Ingestion Script Plan

Input: data/raw/\*.csv or .json (synthetic logs)

Steps in the script:

1.Read all raw log files
2.Convert timestamps to consistent format
3.Extract necessary fields:

timestamp, user, host, event_id, process_name, command_line, source_ip

4.Add optional enrichment (host criticality, AD group membership)
5.Save processed logs to data/processed/clean_logs.csv

Output: Clean CSV ready for feature engineering.

step 1:
Create synthetic log file using excel and saving it as csv file into /data/raw folder.

step 2:
create python ingestion script "src/ingestion/log_ingestion.py"

The script will:

1.Read CSV files from data/raw/
2.Normalize timestamps to datetime objects
3.Select required columns for the pipeline
4.Save clean data to data/processed/clean_logs.csv

Phase 0: Step 2 - First Rule-Based Detection System.

What is Rule-Based Detection?
Using hard coded rules to detect suspicous activity.

Example rule:
Suspicous login outside working hours.
Multiple logins to different hosts in short time (idicates lateral movement possibility)
Remote process creation (powershell.exe)
Access to sensitive hosts by uncommon users. ( HR server accessed by finance user)

Step 1:
Create a new script into "src/detection/rule_based_detection.py"
Step 2:
inputs -- data/processed/clean_logs.csv
outputs -- data/alerts/alerts.csv
step 3:
run script from main folder.

Phase 1: ML-Based Detection

Machine learning :
Train a machine learning model to detect anomalous user behavior, like lateral movement or suspicious logins, wihtout hard-coded rules.

Using Isolation forest -- detects outliers in high-dimensional data; good for logs

Feature Engineering: selecting most revelant features(individual measurable properties that model uses as input to make predictions) from the data and craeting new ones to improve model's performance.

Data Splitting: Dividing the dataset into training, validation, and testing sets.

Model Training: Choosing an algorithm and training it on the prepared data.

Model Evaluation: Testing the trained model's performance using metrics like accuracy, precision, and recall to see how well it generalizes.

Model Deployment: Making the final model available to be used in a production environment, often through an API or cloud service.

Model Maintenance: Continuously monitoring and updating the model after deployment to ensure it remains effective.

Step 1: Feature Engineering
Step 2: Labeling
Step 3: Choosing an ML Model
Step 4: ML pipeline
Read data/processed/clean_logs.csv
Generate features per user per time window
Fit the model (Isolation Forest) on normal/synthetic data
Predict anomalies → output alerts
Save alerts to data/alerts/ml_alerts.csv
Step 5: Output
