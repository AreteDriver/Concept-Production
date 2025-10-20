"""
Toyota Production 2.0 - AI-driven QA/Lean System
Main application entry point for the Streamlit dashboard.
"""

import logging
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np

try:
    from config import config
except ImportError:
    config = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Toyota Production 2.0",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=60)
def generate_sample_metrics():
    """Generate sample metrics data for demonstration."""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    data = {
        'Date': dates,
        'Cycle Time (hrs)': np.random.normal(24, 3, 30),
        'QA Issues': np.random.poisson(5, 30),
        'Production Units': np.random.normal(100, 10, 30),
        'Efficiency (%)': np.random.normal(85, 5, 30)
    }
    return pd.DataFrame(data)


def render_sidebar():
    """Render the sidebar with navigation and status."""
    with st.sidebar:
        # Display header with emoji instead of external image
        st.markdown("## 🏭 TPS 2.0")
        st.markdown("---")
        
        st.header("📋 Navigation")
        
        page = st.radio(
            "Select View:",
            ["🏠 Dashboard", "📊 Metrics", "🤖 AI Guidance", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        st.subheader("System Status")
        st.success("✅ System Online")
        st.metric("Uptime", "99.9%", "+0.1%")
        
        st.markdown("---")
        
        st.caption("""
        **TLS Concept v2.0**  
        AI-driven QA/Lean System  
        © 2025 AreteDriver
        """)
        
        return page


def render_dashboard():
    """Render the main dashboard view."""
    st.title("🏭 Toyota Production 2.0 — AI + Lean Demo")
    
    st.markdown("""
    ### Problem Statement
    Reduce install/QA cycle time with AI guidance and live metrics.
    
    ### Process Flow
    **AI → Data Layer → AR Interface → Human Feedback**
    """)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Cycle Time", "22.5 hrs", "-1.5 hrs", delta_color="inverse")
    
    with col2:
        st.metric("QA Issues", "47", "-8", delta_color="inverse")
    
    with col3:
        st.metric("Production Units", "2,847", "+127")
    
    with col4:
        st.metric("Efficiency", "87.3%", "+2.3%")
    
    st.markdown("---")
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Recent Trends")
        df = generate_sample_metrics()
        st.line_chart(df.set_index('Date')[['Cycle Time (hrs)', 'Efficiency (%)']])
        
    with col2:
        st.subheader("🔔 Recent Alerts")
        st.warning("⚠️ Cycle time spike detected in Assembly Line 3")
        st.info("ℹ️ Maintenance scheduled for tomorrow 2:00 AM")
        st.success("✅ Quality targets met for 7 consecutive days")


def render_metrics():
    """Render the detailed metrics view."""
    st.title("📊 Detailed Metrics")
    
    df = generate_sample_metrics()
    
    # Date range selector
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Time Series Analysis")
    with col2:
        period = st.selectbox("Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days"])
    
    # Display metrics
    tabs = st.tabs(["Cycle Time", "Quality", "Production", "Efficiency"])
    
    with tabs[0]:
        st.line_chart(df.set_index('Date')['Cycle Time (hrs)'])
        st.dataframe(df[['Date', 'Cycle Time (hrs)']].tail(10))
    
    with tabs[1]:
        st.bar_chart(df.set_index('Date')['QA Issues'])
        st.dataframe(df[['Date', 'QA Issues']].tail(10))
    
    with tabs[2]:
        st.area_chart(df.set_index('Date')['Production Units'])
        st.dataframe(df[['Date', 'Production Units']].tail(10))
    
    with tabs[3]:
        st.line_chart(df.set_index('Date')['Efficiency (%)'])
        st.dataframe(df[['Date', 'Efficiency (%)']].tail(10))


def render_ai_guidance():
    """Render the AI guidance view."""
    st.title("🤖 AI Guidance & Recommendations")
    
    st.info("🚧 AI features are currently under development. OpenAI integration coming soon.")
    
    st.subheader("Upcoming AI Features")
    
    features = [
        ("🎯", "Predictive Analytics", "Forecast production issues before they occur"),
        ("💡", "Smart Recommendations", "AI-powered suggestions for process optimization"),
        ("🔍", "Root Cause Analysis", "Automated analysis of quality issues"),
        ("📋", "Automated Reporting", "Generate insights and reports automatically"),
        ("🤝", "Natural Language Interface", "Ask questions in plain English")
    ]
    
    for icon, title, description in features:
        with st.expander(f"{icon} {title}"):
            st.write(description)
            st.progress(0.3, "30% Complete")


def render_settings():
    """Render the settings view."""
    st.title("⚙️ Settings & Configuration")
    
    st.subheader("Feature Flags")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Enable AI Guidance", value=False, disabled=True)
        st.checkbox("Enable Metrics Dashboard", value=True)
        st.checkbox("Enable AR Interface", value=False, disabled=True)
    
    with col2:
        st.checkbox("Enable Notifications", value=True)
        st.checkbox("Enable Data Export", value=True)
        st.checkbox("Enable Advanced Analytics", value=False)
    
    st.markdown("---")
    
    st.subheader("System Configuration")
    
    st.text_input("API Endpoint", placeholder="https://api.example.com")
    st.select_slider("Log Level", options=["DEBUG", "INFO", "WARNING", "ERROR"], value="INFO")
    
    if st.button("Save Configuration"):
        st.success("✅ Configuration saved successfully!")


def main():
    """Main application function."""
    try:
        # Render sidebar and get selected page
        page = render_sidebar()
        
        # Route to appropriate view
        if page == "🏠 Dashboard":
            render_dashboard()
        elif page == "📊 Metrics":
            render_metrics()
        elif page == "🤖 AI Guidance":
            render_ai_guidance()
        elif page == "⚙️ Settings":
            render_settings()
        
        logger.info(f"Application loaded successfully - Page: {page}")
        
    except Exception as e:
        logger.error(f"Error in main application: {e}", exc_info=True)
        st.error(f"An error occurred: {e}")
        st.info("Please refresh the page or contact support if the issue persists.")


if __name__ == "__main__":
    main()
