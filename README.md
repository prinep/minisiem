# MiniSIEM

A lightweight Security Information and Event Management (SIEM) system built with Python.

## Features

- Parses SSH, web, and network logs
- Detects brute-force attacks
- Detects successful logins after brute-force attempts
- Detects suspicious path traversal requests
- Detects potential port scans
- Assigns risk scores to security alerts
- Correlates alerts by source IP
- Stores events and alerts using SQLite
- Provides a CLI dashboard for security analysis

## Architecture

```text
Log Files
    ↓
Log Parser
    ↓
Event Detection Engine
    ↓
Alert Generation
    ↓
Risk Scoring
    ↓
Event Correlation
    ↓
SQLite Database
    ↓
CLI Dashboard