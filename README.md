# 🛡️ MiniSIEM

A lightweight Security Information and Event Management (SIEM) system built with Python for log analysis, threat detection, alerting, and incident correlation.

## Features

- Parses SSH, web, and network logs
- Detects brute-force attacks
- Detects successful logins after brute-force attempts
- Detects unusual login times
- Detects path traversal attempts
- Detects potential port scans
- Assigns risk scores to detected threats
- Correlates alerts by source IP
- Stores events, alerts, and incidents in SQLite
- Provides a CLI monitoring interface
- Provides a Streamlit web dashboard

## Architecture

```text
Log Files
    ↓
Log Parser
    ↓
Detection Engine
    ↓
Alerts + Risk Scoring
    ↓
Incident Correlation
    ↓
SQLite Database
    ↓
CLI / Streamlit Dashboard