import streamlit as st
from utils.styles import section_header, metric_card, ai_insight_box
from utils.services import get_insight

def render_home():
    st.markdown("## 🏥 Clinical Intelligence Platform")
    st.markdown(
        """
        **An AI-powered Clinical & Operational Intelligence Layer**  
        Turning fragmented healthcare data into decisions, not dashboards.
        """
    )

    # Move login to sidebar
    with st.sidebar:
        section_header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username == "admin" and password == "admin":
                st.session_state.user_role = "admin"
                st.rerun()
            elif username == "doctor" and password == "doctor":
                st.session_state.user_role = "doctor"
                st.rerun()
            else:
                st.error("Invalid credentials")

    section_header("AI Health System Diagnosis")
    ai_insight_box(
        "System-Level Insight",
        get_insight("admin_data", "ai_executive_brief")
    )
    """
    section_header("What AI Is Watching Right Now")
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Patients Trending to High Risk", get_insight("admin_data", "high_risk_cohort"))
    with col2:
        metric_card("Insurance Instability Signals", "18% of chronic cohort")
    with col3:
        metric_card("Rising Preventive Care Gaps", "Metabolic & Respiratory Pathways")

    st.info("These signals are continuously monitored by the AI reasoning layer to surface emerging risks before they escalate.")
    """

    # Footer with AI governance note
    st.markdown("---")
    st.caption("Powered by LLM for intelligent narratives and CrewAI for agentic orchestration. Explainable, governable, and built for enterprise healthcare.")