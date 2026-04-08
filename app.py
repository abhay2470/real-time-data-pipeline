import streamlit as st
import pandas as pd
import boto3
import json
from datetime import datetime

# PAGE CONFIG
st.set_page_config(page_title="Real-Time Dashboard", layout="wide")

st.title("📊 Real-Time Weather Data Dashboard")

# AUTO REFRESH
st.caption("Auto-refreshes every time you reload 🔄")

# AWS S3 CONNECTION
s3 = boto3.client('s3')
bucket = "project-realtime-data-pipeline"

# LOAD DATA
objects = s3.list_objects_v2(Bucket=bucket)

data_list = []

for obj in objects.get("Contents", []):
    file = s3.get_object(Bucket=bucket, Key=obj["Key"])
    content = json.loads(file["Body"].read())
    data_list.append(content)

df = pd.DataFrame(data_list)

# SORT BY TIME
df["time"] = pd.to_datetime(df["time"])
df = df.sort_values("time")

# METRICS
col1, col2, col3 = st.columns(3)

col1.metric("🌡️ Latest Temp", f"{df['temperature'].iloc[-1]} °C")
col2.metric("💨 Wind Speed", f"{df['windspeed'].iloc[-1]} km/h")
col3.metric("📅 Records", len(df))

st.divider()

# CHARTS
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ Temperature Trend")
    st.line_chart(df.set_index("time")["temperature"])

with col2:
    st.subheader("💨 Wind Speed Trend")
    st.line_chart(df.set_index("time")["windspeed"])

st.divider()

# DATA TABLE
st.subheader("📄 Raw Data")
st.dataframe(df, use_container_width=True)