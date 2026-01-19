import streamlit as st

def inject_css():
    st.markdown(
        """
        <style>
        .main { background-color: #F9FAFB; }
        .sidebar .sidebar-content { background-color: #1E3A8A; color: #FFFFFF; }
        .stButton > button { background-color: #2DD4BF; color: #1E3A8A; border-radius: 8px; }
        .metric-card { background-color: #FFFFFF; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .ai-insight-box { background-color: #E6FFFA; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
        h1, h2, h3 { color: #1E3A8A; }
        </style>
        """,
        unsafe_allow_html=True
    )

def section_header(text):
    st.markdown(f"## {text}")

def metric_card(label, value):
    st.markdown(f'<div class="metric-card"><b>{label}</b><br>{value}</div>', unsafe_allow_html=True)

def ai_insight_box(title, text):
    st.markdown(f'<div class="ai-insight-box"><b>{title}</b><br>{text}</div>', unsafe_allow_html=True)

# Inject CSS globally (call this in dashboard.py)