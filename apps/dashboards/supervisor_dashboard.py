"""Supervisor Dashboard for TLS AI/AR Production System."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="TLS Production Dashboard",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 TLS AI/AR Production Dashboard")
st.markdown("Real-time monitoring of install, QA, and yard operations")

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Date Range",
    value=(datetime.now() - timedelta(days=7), datetime.now())
)
shift_filter = st.sidebar.selectbox(
    "Shift",
    ["All", "Day Shift", "Night Shift"]
)
line_filter = st.sidebar.multiselect(
    "Production Lines",
    ["Line 1", "Line 2", "Line 3", "QA Lane A", "QA Lane B"],
    default=["Line 1", "Line 2"]
)

# Generate mock data for demonstration
@st.cache_data
def generate_mock_data():
    """Generate mock production data."""
    dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='H')
    
    data = {
        'timestamp': dates,
        'vehicles_completed': [random.randint(2, 8) for _ in range(len(dates))],
        'cycle_time_minutes': [random.randint(45, 90) for _ in range(len(dates))],
        'first_time_through': [random.uniform(0.85, 0.98) for _ in range(len(dates))],
        'defects_found': [random.randint(0, 3) for _ in range(len(dates))],
    }
    
    return pd.DataFrame(data)

df = generate_mock_data()

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Units Completed Today",
        value=145,
        delta="+12 vs yesterday"
    )

with col2:
    st.metric(
        label="Avg Cycle Time",
        value="67 min",
        delta="-5 min vs target"
    )

with col3:
    st.metric(
        label="First-Time-Through Rate",
        value="94.2%",
        delta="+2.1%"
    )

with col4:
    st.metric(
        label="Open Defects",
        value=8,
        delta="-3"
    )

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Cycle Time Trend")
    fig_cycle = px.line(
        df,
        x='timestamp',
        y='cycle_time_minutes',
        title='Average Cycle Time by Hour'
    )
    fig_cycle.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Target: 70min")
    st.plotly_chart(fig_cycle, use_container_width=True)

with col2:
    st.subheader("✅ First-Time-Through Rate")
    fig_ftt = px.line(
        df,
        x='timestamp',
        y='first_time_through',
        title='FTT Rate Over Time',
        range_y=[0.8, 1.0]
    )
    fig_ftt.add_hline(y=0.90, line_dash="dash", line_color="green", annotation_text="Target: 90%")
    st.plotly_chart(fig_ftt, use_container_width=True)

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚗 Throughput by Hour")
    fig_throughput = px.bar(
        df,
        x='timestamp',
        y='vehicles_completed',
        title='Vehicles Completed per Hour'
    )
    st.plotly_chart(fig_throughput, use_container_width=True)

with col2:
    st.subheader("⚠️ Defects by Category")
    defect_data = pd.DataFrame({
        'Category': ['Paint/Body', 'Decal Alignment', 'Torque', 'Missing Parts', 'Other'],
        'Count': [15, 8, 5, 3, 7]
    })
    fig_defects = px.pie(
        defect_data,
        names='Category',
        values='Count',
        title='Defects Distribution (Last 7 Days)'
    )
    st.plotly_chart(fig_defects, use_container_width=True)

# Detailed Tables
st.subheader("🔍 Active Vehicles Status")

# Mock active vehicles data
active_vehicles = pd.DataFrame({
    'VIN': [f'1HGCM8263{i}A{j:06d}' for i, j in enumerate([(123456 + i) for i in range(10)])],
    'Model': ['Camry', 'RAV4', 'Highlander', 'Corolla', 'Tacoma', 'Camry', 'RAV4', 'Tundra', 'Sienna', 'Camry'],
    'Status': ['Install', 'QA', 'Yard', 'Install', 'Install', 'QA', 'Yard', 'Install', 'QA', 'Shipped'],
    'Progress': ['75%', '100%', '100%', '45%', '60%', '100%', '100%', '30%', '100%', '100%'],
    'Assigned To': ['John D.', 'Sarah M.', 'Mike R.', 'John D.', 'Lisa K.', 'Sarah M.', 'Mike R.', 'John D.', 'Sarah M.', 'N/A'],
    'Time in Stage': ['45 min', '10 min', '2 hrs', '30 min', '55 min', '5 min', '3 hrs', '20 min', '8 min', 'N/A']
})

st.dataframe(active_vehicles, use_container_width=True)

# Labor & Capacity Section
st.subheader("👷 Labor & Capacity")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Active Workers",
        value=24,
        delta="+2 vs scheduled"
    )

with col2:
    st.metric(
        label="Certified Installers",
        value=18,
        delta="75% of workforce"
    )

with col3:
    st.metric(
        label="Yard Capacity Used",
        value="68%",
        delta="6,800 / 10,000 units"
    )

# Yard Dock Status
st.subheader("🚢 Dock Status")

dock_status = pd.DataFrame({
    'Dock': ['Dock 1', 'Dock 2', 'Dock 3', 'Dock 4'],
    'Capacity': [2500, 2500, 2500, 2500],
    'Current': [1850, 2100, 1650, 1200],
    'Available': [650, 400, 850, 1300],
    'Utilization': ['74%', '84%', '66%', '48%']
})

fig_dock = px.bar(
    dock_status,
    x='Dock',
    y=['Current', 'Available'],
    title='Dock Capacity Overview',
    barmode='stack',
    color_discrete_map={'Current': 'steelblue', 'Available': 'lightgray'}
)
st.plotly_chart(fig_dock, use_container_width=True)

# Recent Alerts
st.subheader("🔔 Recent Alerts & Events")

alerts = pd.DataFrame({
    'Time': ['2 min ago', '15 min ago', '45 min ago', '1 hr ago', '2 hrs ago'],
    'Type': ['Warning', 'Info', 'Critical', 'Info', 'Warning'],
    'Message': [
        'High torque variance detected on Line 2 - Step 7',
        'QA walkaround completed for VIN 1HGCM82633A789012 - Green',
        'Critical defect: Paint scratch on VIN 1HGCM82633A456789',
        'Hot unit arrived: VIN 1HGCM82633A111222 - Priority processing',
        'Parts shortage warning: Window decal stock low (< 50 units)'
    ]
})

# Color code by type
def highlight_alerts(row):
    if row['Type'] == 'Critical':
        return ['background-color: #ffcccc'] * len(row)
    elif row['Type'] == 'Warning':
        return ['background-color: #fff3cd'] * len(row)
    else:
        return ['background-color: #d1ecf1'] * len(row)

st.dataframe(alerts.style.apply(highlight_alerts, axis=1), use_container_width=True)

# Training & Certifications
st.subheader("📚 Training & Certifications")

training_data = pd.DataFrame({
    'Certification': ['Basic Install', 'Torque Certified', 'QA Certified', 'AR System', 'Hot Unit Handler'],
    'Certified': [22, 18, 8, 20, 12],
    'In Training': [2, 3, 4, 4, 2],
    'Required': [24, 20, 10, 24, 15]
})

fig_training = go.Figure(data=[
    go.Bar(name='Certified', x=training_data['Certification'], y=training_data['Certified']),
    go.Bar(name='In Training', x=training_data['Certification'], y=training_data['In Training']),
    go.Bar(name='Gap', x=training_data['Certification'], 
           y=training_data['Required'] - training_data['Certified'] - training_data['In Training'])
])

fig_training.update_layout(barmode='stack', title='Certification Coverage by Type')
st.plotly_chart(fig_training, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("🔄 Dashboard auto-refreshes every 30 seconds | Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
