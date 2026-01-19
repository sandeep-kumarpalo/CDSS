import streamlit as st
import pandas as pd
from utils.styles import section_header, metric_card, ai_insight_box
from utils.charts import risk_distribution_chart, cost_treemap_chart, equity_heatmap_chart, care_flow_sankey, hospitalization_scatter
from utils.services import get_insight, derive_insight_via_agents

def render_admin_dashboard():
    # Logout in sidebar
    with st.sidebar:
        if st.button("Logout"):
            del st.session_state.user_role
            st.rerun()

    st.markdown("## 🏥 Hospital Intelligence – Admin View")
    st.markdown("Population-level clinical intelligence derived from longitudinal records. All insights are de-identified and HIPAA-safe.")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Executive Overview",
        "⚠️ Risk Stratification",
        "🔁 Care Coordination",
        "💰 Cost & Insurance Intelligence",
        "🔮 Predictive & What-If Analytics",
        "🧠 AI Strategy Console"
    ])

    # TAB 1 — Executive Overview
    with tab1:
        section_header("Executive Overview – Why the system is under stress")
        ai_insight_box("AI Executive Brief", get_insight("admin_data", "ai_executive_brief"))

        cols = st.columns(4)
        metrics = get_insight("admin_data", "key_metrics")
        cols[0].metric("Patients Analyzed", metrics["patients_analyzed"])
        cols[1].metric("High-Risk Cohort", f"~{metrics['high_risk_percentage']}%")
        cols[2].metric("Avoidable Cost Index", metrics["avoidable_cost_index"])
        cols[3].metric("AI Confidence", metrics["ai_confidence"])

        st.plotly_chart(risk_distribution_chart(get_insight("admin_data", "risk_distribution")), use_container_width=True)
        st.caption("**Interpretation:** The 19% High Risk cohort drives the majority of resource intensity. Focusing interventions here yields the highest ROI.")
        st.caption("*Note: Avoidable Cost Index represents the ratio of costs associated with potentially preventable events (e.g., emergency visits for chronic conditions) to total care costs. A score > 0.5 indicates significant opportunity for savings.*")

    # TAB 2 — Risk Stratification
    with tab2:
        section_header("Risk Stratification – From populations to priorities")
        ai_insight_box("AI Root Cause Insight", get_insight("admin_data", "ai_root_cause_insight"))

        st.subheader("Risk Ownership Lens")
        st.dataframe(get_insight("admin_data", "risk_ownership_lens"))

        st.plotly_chart(equity_heatmap_chart(get_insight("admin_data", "equity_heatmap")["disparities"]), use_container_width=True)
        st.caption("**Interpretation:** Darker areas indicate compounding risk factors. Urban and Hispanic cohorts show higher instability, suggesting that social determinants and insurance churn are amplifying clinical risk in these groups.")

    # TAB 3 — Care Coordination
    with tab3:
        section_header("Care Coordination – Where the system breaks")
        ai_insight_box("AI Care Breakdown Prediction", get_insight("admin_data", "ai_care_breakdown_prediction"))
        ai_insight_box("AI Failure Pattern Insight", get_insight("admin_data", "ai_failure_pattern_insight"))

        st.plotly_chart(care_flow_sankey(), use_container_width=True)
        st.caption("**Interpretation:** The flow thickness represents patient volume. Note the significant diversion from Primary Care to Emergency, bypassing Specialists—a hallmark of fragmented coordination.")

    # TAB 4 — Cost & Insurance Intelligence
    with tab4:
        section_header("Cost & Insurance Intelligence – The hidden engine of risk")
        ai_insight_box("AI Financial Leakage Insight", get_insight("admin_data", "ai_financial_leakage_insight"))

        cost_data = get_insight("admin_data", "cost_treemap_data")
        st.plotly_chart(cost_treemap_chart(cost_data["labels"], cost_data["values"]), use_container_width=True)
        st.caption("**Interpretation:** Medications are the primary cost driver, followed by Encounters. The high medication spend relative to outcomes suggests adherence issues or lack of generic utilization.")

        st.metric("Avoidable Cost Index", get_insight("admin_data", "avoidable_cost_index"))
        st.caption("*Note: Avoidable Cost Index (0.68) indicates that nearly 68% of acute costs could be mitigated through better upstream preventive care and coordination.*")

    # TAB 5 — Predictive & What-If Analytics
    with tab5:
        section_header("Predictive & What-If Analytics – Futures, not reports")
        ai_insight_box("AI Forecast", get_insight("admin_data", "ai_forecast"))
        ai_insight_box("Counterfactual Intelligence", get_insight("admin_data", "counterfactual_intelligence"))

        #st.plotly_chart(hospitalization_scatter(get_insight("admin_data", "hospitalization_risk_distribution")), use_container_width=True)
        #st.caption("**Interpretation:** Higher risk scores correlate with age, but significant variance exists. Young patients with high risk scores (outliers) represent the 'Preventive Failure' archetype.")

    # TAB 6 — AI Strategy Console
    with tab6:
        section_header("AI Strategy Console – Why this is scalable AI")
        prompts = get_insight("admin_data", "pre_loaded_prompts")
        for prompt in prompts:
            with st.expander(prompt):
                st.write("AI Response: " + derive_insight_via_agents(prompt))  # Simulated or real

        ai_gov = get_insight("admin_data", "ai_governance")
        st.subheader("AI Governance & Trust Panel")
        for key, value in ai_gov.items():
            st.markdown(f"- **{key.capitalize()}**: {value}")

        with st.expander("Confidence & Limitations"):
            conf_lim = get_insight("doctor", "confidence_and_limitations")
            if isinstance(conf_lim, dict):  # Check if dict
                st.subheader("Confidence")
                for c in conf_lim.get("confidence", []):
                    st.markdown(f"- {c}")
                st.subheader("Limitations")
                for l in conf_lim.get("limitations", []):
                    st.markdown(f"- {l}")
                st.caption(conf_lim.get("disclaimer", ""))
            else:
                st.write("Confidence data not available.")

        st.subheader("Hero Insights")
        hero_insights = get_insight("admin_data", "ai_alerts")
        if isinstance(hero_insights, list):
            for alert in hero_insights:
                ai_insight_box("Strategic Alert", alert)
        else:
            st.write("Hero insights data not available.")

        agent_fn = get_insight("doctor", "agent_footnote")
        st.subheader("Agent Footnote")
        if isinstance(agent_fn, dict):  # Check if dict
            st.write(f"Agents Involved: {agent_fn.get('agents_involved', 'Not available')}")
            st.write(f"Datasets Analyzed: {agent_fn.get('datasets_analyzed', 'Not available')}")
            st.write(f"Population Context: {agent_fn.get('population_context', 'Not available')}")
            st.dataframe(pd.DataFrame(agent_fn.get("agent_details", [])))
        else:
            st.write("Agent footnote data not available.")