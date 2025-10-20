"""Logistics Planning Dashboard for Yard Management."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="TLS Logistics Planner",
    page_icon="📦",
    layout="wide"
)

st.title("📦 TLS Logistics & Yard Planning System")
st.markdown("Strategic planning for 140,000 VINs across 4 docks (2,500 units each)")

# Sidebar - Planning Parameters
st.sidebar.header("Planning Parameters")

daily_throughput_goal = st.sidebar.number_input(
    "Daily Throughput Goal",
    min_value=50,
    max_value=500,
    value=200,
    step=10
)

available_installers = st.sidebar.number_input(
    "Available Installers",
    min_value=5,
    max_value=50,
    value=24,
    step=1
)

available_qa_staff = st.sidebar.number_input(
    "Available QA Staff",
    min_value=2,
    max_value=20,
    value=8,
    step=1
)

available_shuttle_drivers = st.sidebar.number_input(
    "Available Shuttle Drivers",
    min_value=2,
    max_value=15,
    value=6,
    step=1
)

avg_install_time = st.sidebar.slider(
    "Avg Install Time (minutes)",
    min_value=30,
    max_value=120,
    value=65,
    step=5
)

# Calculate capacity
working_hours_per_day = 16  # Two shifts
minutes_per_day = working_hours_per_day * 60

installer_capacity = (available_installers * minutes_per_day) / avg_install_time
qa_capacity = available_qa_staff * (working_hours_per_day * 60 / 15)  # 15 min per QA
shuttle_capacity = available_shuttle_drivers * (working_hours_per_day * 60 / 8)  # 8 min per move

# Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🔧 Install Capacity/Day",
        value=f"{int(installer_capacity)}",
        delta=f"{int(installer_capacity - daily_throughput_goal)} vs goal"
    )

with col2:
    st.metric(
        label="✅ QA Capacity/Day",
        value=f"{int(qa_capacity)}",
        delta=f"{int(qa_capacity - daily_throughput_goal)} vs goal"
    )

with col3:
    st.metric(
        label="🚗 Shuttle Capacity/Day",
        value=f"{int(shuttle_capacity)}",
        delta=f"{int(shuttle_capacity - daily_throughput_goal)} vs goal"
    )

with col4:
    bottleneck = min(installer_capacity, qa_capacity, shuttle_capacity)
    st.metric(
        label="⚠️ System Bottleneck",
        value=f"{int(bottleneck)} units/day",
        delta=f"{int(bottleneck - daily_throughput_goal)} vs goal"
    )

# Dock Overview
st.header("🚢 Dock Allocation & Status")

dock_data = pd.DataFrame({
    'Dock': ['Dock 1', 'Dock 2', 'Dock 3', 'Dock 4'],
    'Capacity': [2500, 2500, 2500, 2500],
    'Current': [1850, 2100, 1650, 1200],
    'Reserved': [400, 300, 600, 800],
    'Available': [250, 100, 250, 500],
    'Hot Units': [15, 8, 12, 5],
    'Parts Ready': [1650, 1900, 1400, 1000],
    'Parts Pending': [200, 200, 250, 200]
})

col1, col2 = st.columns(2)

with col1:
    fig_dock_capacity = px.bar(
        dock_data,
        x='Dock',
        y=['Current', 'Reserved', 'Available'],
        title='Dock Capacity Breakdown',
        barmode='stack',
        color_discrete_map={
            'Current': 'steelblue',
            'Reserved': 'orange',
            'Available': 'lightgray'
        }
    )
    st.plotly_chart(fig_dock_capacity, use_container_width=True)

with col2:
    fig_parts_status = px.bar(
        dock_data,
        x='Dock',
        y=['Parts Ready', 'Parts Pending'],
        title='Parts Availability by Dock',
        barmode='stack',
        color_discrete_map={
            'Parts Ready': 'green',
            'Parts Pending': 'red'
        }
    )
    st.plotly_chart(fig_parts_status, use_container_width=True)

st.dataframe(dock_data, use_container_width=True)

# Incoming Vehicle Management
st.header("📥 Incoming Vehicle Management")

# Mock incoming data
incoming_vins = pd.DataFrame({
    'VIN': [f'VIN{i:07d}' for i in range(1, 21)],
    'Model': random.choices(['Camry', 'RAV4', 'Highlander', 'Tacoma', 'Tundra'], k=20),
    'Priority': random.choices(['Standard', 'Hot', 'Critical'], weights=[15, 4, 1], k=20),
    'Parts Status': random.choices(['Ready', 'Partial', 'Pending'], weights=[12, 5, 3], k=20),
    'Assigned Dock': random.choices(['Dock 1', 'Dock 2', 'Dock 3', 'Dock 4'], k=20),
    'Parking Position': [f'P{random.randint(1, 100):03d}' for _ in range(20)],
    'Est. Start Date': [(datetime.now() + timedelta(days=random.randint(0, 5))).strftime('%Y-%m-%d') for _ in range(20)]
})

# Color code by priority
def highlight_priority(row):
    if row['Priority'] == 'Critical':
        return ['background-color: #dc3545; color: white'] * len(row)
    elif row['Priority'] == 'Hot':
        return ['background-color: #ffc107'] * len(row)
    else:
        return [''] * len(row)

st.dataframe(incoming_vins.style.apply(highlight_priority, axis=1), use_container_width=True)

# Optimization Recommendations
st.header("💡 Optimization Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Resource Allocation")
    
    # Calculate recommendations
    if installer_capacity < daily_throughput_goal:
        st.warning(f"⚠️ Need {int((daily_throughput_goal - installer_capacity) * avg_install_time / (working_hours_per_day * 60))} more installers")
    else:
        st.success("✅ Install capacity meets goal")
    
    if qa_capacity < daily_throughput_goal:
        st.warning(f"⚠️ Need {int((daily_throughput_goal - qa_capacity) / (working_hours_per_day * 4))} more QA staff")
    else:
        st.success("✅ QA capacity meets goal")
    
    if shuttle_capacity < daily_throughput_goal:
        st.warning(f"⚠️ Need {int((daily_throughput_goal - shuttle_capacity) / (working_hours_per_day * 7.5))} more shuttle drivers")
    else:
        st.success("✅ Shuttle capacity meets goal")

with col2:
    st.subheader("Dock Optimization")
    
    # Find dock with most hot units
    max_hot_dock = dock_data.loc[dock_data['Hot Units'].idxmax(), 'Dock']
    st.info(f"🔥 {max_hot_dock} has the most hot units - prioritize resources there")
    
    # Find dock with most parts pending
    max_pending_dock = dock_data.loc[dock_data['Parts Pending'].idxmax(), 'Dock']
    st.warning(f"📦 {max_pending_dock} has the most parts pending - expedite parts delivery")
    
    # Find dock with most available space
    max_space_dock = dock_data.loc[dock_data['Available'].idxmax(), 'Dock']
    st.success(f"✨ {max_space_dock} has the most available space - route new arrivals there")

# Daily Plan Simulation
st.header("📅 Daily Production Plan")

plan_data = pd.DataFrame({
    'Hour': list(range(6, 22)),  # 6 AM to 10 PM
    'Planned Installs': [random.randint(10, 15) for _ in range(16)],
    'Planned QA': [random.randint(8, 14) for _ in range(16)],
    'Planned Shuttles': [random.randint(5, 12) for _ in range(16)]
})

fig_plan = go.Figure()
fig_plan.add_trace(go.Scatter(x=plan_data['Hour'], y=plan_data['Planned Installs'], 
                              mode='lines+markers', name='Installs'))
fig_plan.add_trace(go.Scatter(x=plan_data['Hour'], y=plan_data['Planned QA'], 
                              mode='lines+markers', name='QA'))
fig_plan.add_trace(go.Scatter(x=plan_data['Hour'], y=plan_data['Planned Shuttles'], 
                              mode='lines+markers', name='Shuttles'))

fig_plan.update_layout(
    title='Hourly Production Plan',
    xaxis_title='Hour of Day',
    yaxis_title='Units',
    hovermode='x unified'
)

st.plotly_chart(fig_plan, use_container_width=True)

# Parts Inventory Summary
st.header("📦 Parts Inventory Status")

parts_data = pd.DataFrame({
    'Part Category': ['Decals', 'Accessories', 'Electronics', 'Hardware', 'Fluids'],
    'In Stock': [4500, 3200, 2800, 5600, 1200],
    'Reserved': [1200, 800, 600, 1400, 300],
    'Available': [3300, 2400, 2200, 4200, 900],
    'Reorder Point': [2000, 1500, 1000, 3000, 500]
})

fig_parts = px.bar(
    parts_data,
    x='Part Category',
    y=['Available', 'Reserved'],
    title='Parts Inventory Overview',
    barmode='stack'
)

# Add reorder point line
for i, row in parts_data.iterrows():
    fig_parts.add_hline(
        y=row['Reorder Point'],
        line_dash="dash",
        line_color="red",
        annotation_text=f"Reorder: {row['Reorder Point']}"
    )

st.plotly_chart(fig_parts, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(f"📊 System Bottleneck: **{int(bottleneck)} units/day** | " + 
            f"Daily Goal: **{daily_throughput_goal} units/day** | " +
            f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
