import sys
sys.path.append("src")

from database import Database
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="MiniSIEM",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ MiniSIEM")
st.caption("Security Monitoring Dashboard")

connection = sqlite3.connect("minisiem.db")

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM events")
total_events = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM alerts")
total_alerts = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM alerts WHERE severity = 'HIGH'"
)
high_alerts = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM alerts WHERE severity = 'CRITICAL'"
)
critical_alerts = cursor.fetchone()[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Events", total_events)
col2.metric("Total Alerts", total_alerts)
col3.metric("High Alerts", high_alerts)
col4.metric("Critical Alerts", critical_alerts)

st.subheader("Recent Events")

cursor = connection.cursor()

cursor.execute("""
    SELECT timestamp, event, username, ip
    FROM events
    ORDER BY id DESC
    LIMIT 10
""")

events = cursor.fetchall()

for event in events:
    st.dataframe(
    pd.DataFrame(
        events,
        columns=["Timestamp", "Event", "Username", "IP"]
    ),
    use_container_width=True,
    hide_index=True
)
st.subheader("Security Alerts")

cursor.execute("""
    SELECT message, severity, ip, rule, risk_score
    FROM alerts
    ORDER BY id DESC
    LIMIT 10
""")

alerts = cursor.fetchall()

for alert in alerts:
    alert_df = pd.DataFrame(
    alerts,
    columns=["Message", "Severity", "IP", "Rule", "Risk Score"]
)

def highlight_severity(row):
    if row["Severity"] == "CRITICAL":
        return ["background-color: #ffcccc"] * len(row)
    elif row["Severity"] == "HIGH":
        return ["background-color: #ffe0b3"] * len(row)
    elif row["Severity"] == "MEDIUM":
        return ["background-color: #fff2b3"] * len(row)
    return [""] * len(row)

st.dataframe(
    alert_df.style.apply(highlight_severity, axis=1),
    use_container_width=True,
    hide_index=True
)
st.subheader("Security Incidents")

cursor.execute("""
    SELECT ip, risk_score, alert_count
    FROM incidents
    ORDER BY risk_score DESC
""")

incidents = cursor.fetchall()

if not incidents:
    st.info("No security incidents detected.")
else:
    for incident in incidents:
        st.write(f"**IP:** `{incident[0]}`")
        st.write(f"**Risk Score:** {incident[1]}")
        st.write(f"**Alerts:** {incident[2]}")
        st.divider()
st.subheader("Incident Risk Overview")

if incidents:
    for incident in incidents:
        st.progress(
            min(incident[1] / 100, 1.0),
            text=f"{incident[0]} — Risk Score: {incident[1]}"
        )

connection.close()