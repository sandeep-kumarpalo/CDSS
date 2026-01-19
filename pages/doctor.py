# pages/doctor.py
import streamlit as st
import pandas as pd
from utils.styles import section_header, ai_insight_box
from utils.charts import patient_risk_gauge, encounter_timeline_chart
from utils.services import get_insight

# Patient-specific evidence (hardcoded for demo based on CSV insights; in prod, derive from agents/CSVs)
def get_conditions(pid):
    conditions_data = {
        "14289f20-085c-4fc8-bdd8-e2074166d91f": pd.DataFrame({"Condition": ["Hypertension", "Prediabetes", "Obesity"], "Status": ["Active", "Active", "Active"]}),
        "8d4c4326-e9de-4f45-9a4c-f8c36bff89ae": pd.DataFrame({"Condition": ["Viral sinusitis", "Acute viral pharyngitis"], "Status": ["Resolved", "Resolved"]}),
        "b58731cc-2d8b-4c2d-b327-4cab771af3ef": pd.DataFrame({"Condition": ["Normal pregnancy", "Forearm fracture"], "Status": ["Resolved", "Resolved"]}),
        "1d604da9-9a81-4ba9-80c2-de3375d59b40": pd.DataFrame({"Condition": ["Chronic sinusitis", "Acute bronchitis"], "Status": ["Active", "Resolved"]}),
        "fca3178e-fb68-41c3-8598-702d3ca68b96": pd.DataFrame({"Condition": ["Chronic congestive heart failure", "Osteoporosis", "Prediabetes"], "Status": ["Active", "Active", "Active"]}),
        "fc817953-cc8b-45db-9c85-7c0ced8fa90d": pd.DataFrame({"Condition": ["Osteoarthritis of knee", "Osteoporosis", "Stroke"], "Status": ["Active", "Active", "Resolved"]})
    }
    return conditions_data.get(pid, pd.DataFrame())

def get_observations(pid):
    observations_data = {
        "14289f20-085c-4fc8-bdd8-e2074166d91f": pd.DataFrame({"Observation": ["Body Height", "Body Weight", "BMI"], "Value": ["170 cm", "85 kg", "29.4"], "Flag": ["Normal", "High", "Overweight"]}),
        "8d4c4326-e9de-4f45-9a4c-f8c36bff89ae": pd.DataFrame({"Observation": ["Blood Pressure", "BMI"], "Value": ["120/80 mmHg", "22.4"], "Flag": ["Normal", "Normal"]}),
        "b58731cc-2d8b-4c2d-b327-4cab771af3ef": pd.DataFrame({"Observation": ["Blood Pressure", "BMI"], "Value": ["118/78 mmHg", "24.5"], "Flag": ["Normal", "Normal"]}),
        "1d604da9-9a81-4ba9-80c2-de3375d59b40": pd.DataFrame({"Observation": ["Blood Pressure", "BMI"], "Value": ["119/82 mmHg", "23.5"], "Flag": ["Normal", "Normal"]}),
        "fca3178e-fb68-41c3-8598-702d3ca68b96": pd.DataFrame({"Observation": ["Blood Pressure", "HbA1c"], "Value": ["140/90 mmHg", "6.0%"], "Flag": ["High", "Elevated"]}),
        "fc817953-cc8b-45db-9c85-7c0ced8fa90d": pd.DataFrame({"Observation": ["Blood Pressure", "QOLS"], "Value": ["130/85 mmHg", "1.0"], "Flag": ["High", "Normal"]})
    }
    return observations_data.get(pid, pd.DataFrame())

def get_encounters(pid):
    encounters_data = {
        "14289f20-085c-4fc8-bdd8-e2074166d91f": pd.DataFrame({"Date": ["2010-01-23", "2011-08-09"], "Type": ["Ambulatory", "Emergency"]}),
        "8d4c4326-e9de-4f45-9a4c-f8c36bff89ae": pd.DataFrame({"Date": ["2011-04-30", "2018-03-05"], "Type": ["Wellness", "Ambulatory"]}),
        "b58731cc-2d8b-4c2d-b327-4cab771af3ef": pd.DataFrame({"Date": ["2014-07-08", "2018-06-15"], "Type": ["Emergency", "Prenatal"]}),
        "1d604da9-9a81-4ba9-80c2-de3375d59b40": pd.DataFrame({"Date": ["2011-05-13", "2012-01-23"], "Type": ["Ambulatory", "Wellness"]}),
        "fca3178e-fb68-41c3-8598-702d3ca68b96": pd.DataFrame({"Date": ["1987-09-27", "1990-03-15"], "Type": ["Inpatient", "Ambulatory"]}),
        "fc817953-cc8b-45db-9c85-7c0ced8fa90d": pd.DataFrame({"Date": ["1957-08-25", "2009-08-08"], "Type": ["Wellness", "Emergency"]})
    }
    return encounters_data.get(pid, pd.DataFrame())

def get_care_gaps(pid):
    care_gaps_data = {
        "14289f20-085c-4fc8-bdd8-e2074166d91f": pd.DataFrame({"Gap": ["Missed lipid screening"], "Duration (days)": [90], "Risk Impact": ["Medium"]}),
        "8d4c4326-e9de-4f45-9a4c-f8c36bff89ae": pd.DataFrame({"Gap": ["Annual wellness check"], "Duration (days)": [180], "Risk Impact": ["Low"]}),
        "b58731cc-2d8b-4c2d-b327-4cab771af3ef": pd.DataFrame({"Gap": ["Bone health screening"], "Duration (days)": [120], "Risk Impact": ["Medium"]}),
        "1d604da9-9a81-4ba9-80c2-de3375d59b40": pd.DataFrame({"Gap": ["Immunization panel"], "Duration (days)": [365], "Risk Impact": ["Low"]}),
        "fca3178e-fb68-41c3-8598-702d3ca68b96": pd.DataFrame({"Gap": ["Diabetes management follow-up"], "Duration (days)": [60], "Risk Impact": ["High"]}),
        "fc817953-cc8b-45db-9c85-7c0ced8fa90d": pd.DataFrame({"Gap": ["Geriatric assessment"], "Duration (days)": [90], "Risk Impact": ["Medium"]})
    }
    return care_gaps_data.get(pid, pd.DataFrame())

def get_insurance(pid):
    insurance_data = {
        "14289f20-085c-4fc8-bdd8-e2074166d91f": pd.DataFrame({"Payer": ["Humana", "UnitedHealthcare"], "Status": ["Active", "Inactive"]}),
        "8d4c4326-e9de-4f45-9a4c-f8c36bff89ae": pd.DataFrame({"Payer": ["Humana", "UnitedHealthcare"], "Status": ["Inactive", "Active"]}),
        "b58731cc-2d8b-4c2d-b327-4cab771af3ef": pd.DataFrame({"Payer": ["Aetna", "Cigna"], "Status": ["Inactive", "Active"]}),
        "1d604da9-9a81-4ba9-80c2-de3375d59b40": pd.DataFrame({"Payer": ["Guardian"], "Status": ["Active"]}),
        "fca3178e-fb68-41c3-8598-702d3ca68b96": pd.DataFrame({"Payer": ["Medicare"], "Status": ["Active"]}),
        "fc817953-cc8b-45db-9c85-7c0ced8fa90d": pd.DataFrame({"Payer": ["Medicare", "Private"], "Status": ["Active", "Inactive"]})
    }
    return insurance_data.get(pid, pd.DataFrame())

def get_medications(pid):
    medications_data = {
        "14289f20-085c-4fc8-bdd8-e2074166d91f": pd.DataFrame({"Medication": ["Hydrochlorothiazide", "Metformin"], "Continuity": ["Stable", "Interrupted"]}),
        "8d4c4326-e9de-4f45-9a4c-f8c36bff89ae": pd.DataFrame({"Medication": ["Etonogestrel Implant"], "Continuity": ["Stable"]}),
        "b58731cc-2d8b-4c2d-b327-4cab771af3ef": pd.DataFrame({"Medication": ["Etonogestrel"], "Continuity": ["Stable"]}),
        "1d604da9-9a81-4ba9-80c2-de3375d59b40": pd.DataFrame({"Medication": ["None"], "Continuity": ["N/A"]}),
        "fca3178e-fb68-41c3-8598-702d3ca68b96": pd.DataFrame({"Medication": ["Metoprolol", "Furosemide"], "Continuity": ["Stable", "Stable"]}),
        "fc817953-cc8b-45db-9c85-7c0ced8fa90d": pd.DataFrame({"Medication": ["None chronic"], "Continuity": ["N/A"]})
    }
    return medications_data.get(pid, pd.DataFrame())

def get_last_visit_summary(pid):
    summaries = {
        "14289f20-085c-4fc8-bdd8-e2074166d91f": "Last visit: Reviewed hypertension meds; BP stable but HbA1c elevated; advised diet changes.",
        "8d4c4326-e9de-4f45-9a4c-f8c36bff89ae": "Last visit: Wellness check; all vitals normal; allergy reviewed.",
        "b58731cc-2d8b-4c2d-b327-4cab771af3ef": "Last visit: Influenza vaccine; fracture healing confirmed; no issues.",
        "1d604da9-9a81-4ba9-80c2-de3375d59b40": "Last visit: Sinusitis follow-up; symptoms resolved; preventive advice given.",
        "fca3178e-fb68-41c3-8598-702d3ca68b96": "Last visit: Cardiac review; meds adjusted; osteoporosis scan scheduled.",
        "fc817953-cc8b-45db-9c85-7c0ced8fa90d": "Last visit: Wellness exam; stroke recovery good; mobility exercises recommended."
    }
    return summaries.get(pid, "No recent visit summary available.")

def render_doctor_dashboard():
    # Logout in sidebar
    with st.sidebar:
        if st.button("Logout"):
            del st.session_state.user_role
            st.rerun()

    st.markdown("## 👨‍⚕️ Clinical Intelligence – Doctor View")
    st.markdown("Patient-centric insights derived from longitudinal records. All data is de-identified.")

    # Sidebar Patient Selector (below logout)
    with st.sidebar:
        section_header("Select Patient")
        hero_patients = get_insight("doctor", "hero_patients")
        # Dropdown with ID only
        selected_pid = st.selectbox("Patient ID", list(hero_patients.keys()))

    if not selected_pid:
        st.warning("Select a patient to view insights.")
        return

    pid = selected_pid
    patient = hero_patients[pid]

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Patient Overview",
        "Clinical Risk & Predictions",
        "Care Gaps & Coordination",
        "Cost & Coverage Impact",
        "AI Clinical Co-Pilot"
    ])

    # TAB 1 — Patient Overview
    with tab1:
        section_header("Patient Overview – The patient, explained")
        st.subheader("Patient Details")
        st.write(f"Name: {patient['name']}")
        st.write(f"Age: {patient['age']}")
        st.write(f"Gender: {patient['gender']}")
        st.write(f"Archetype: {patient['archetype']}")

        st.subheader("Last Visit Summary")
        st.write(get_last_visit_summary(pid))

        ai_insight_box("AI Patient Narrative", patient["ai_patient_state"])

        st.subheader("Conditions")
        st.dataframe(get_conditions(pid), use_container_width=True)

        st.subheader("Observations")
        st.dataframe(get_observations(pid), use_container_width=True)

    # TAB 2 — Clinical Risk & Predictions
    with tab2:
        section_header("Clinical Risk & Predictions")
        ai_insight_box("AI Patient State", patient["ai_patient_state"])

        st.subheader("Risk Gauge")
        st.plotly_chart(patient_risk_gauge(patient["risk_score"]), use_container_width=True)

        ai_insight_box("Prediction", patient["predictions"])

    # TAB 3 — Care Gaps & Coordination
    with tab3:
        section_header("Care Gaps & Coordination")
        ai_insight_box("AI Gap Alert", patient["care_gaps"])

        st.subheader("Suggested Action")
        st.markdown(patient["suggested_action"])

        # st.subheader("Encounter Timeline")
        # st.plotly_chart(encounter_timeline_chart(get_encounters(pid)), use_container_width=True)

        st.subheader("Detected Care Gaps")
        st.dataframe(get_care_gaps(pid), use_container_width=True)

    # TAB 4 — Cost & Coverage Impact
    with tab4:
        section_header("Cost & Coverage Impact (Doctor-Relevant)")
        ai_insight_box("AI Cost & Coverage Insight", patient["cost_coverage_insight"])

        st.subheader("Coverage")
        st.dataframe(get_insurance(pid), use_container_width=True)

        st.subheader("Medication Continuity")
        st.dataframe(get_medications(pid), use_container_width=True)

    # TAB 5 — AI Clinical Co-Pilot
    with tab5:
        section_header("AI Clinical Co-Pilot")
        ai_insight_box("AI Temporal Reasoning", patient["ai_temporal_reasoning"])

        st.subheader("AI-Recommended Focus")
        for item in patient["ai_recommended_focus"]:
            st.markdown(f"- {item}")

        ai_insight_box("AI Conclusion", patient["ai_conclusion"])

        prompts = patient["co_pilot_prompts"]
        for prompt, response in prompts.items():
            with st.expander(prompt):
                st.write(response)

        with st.expander("Confidence & Limitations"):
            conf_lim = patient["confidence_and_limitations"]
            st.subheader("Confidence")
            for c in conf_lim["confidence"]:
                st.markdown(f"- {c}")
            st.subheader("Limitations")
            for l in conf_lim["limitations"]:
                st.markdown(f"- {l}")
            st.caption(conf_lim["disclaimer"])

        agent_fn = get_insight("doctor", "agent_footnote")
        st.subheader("Agent Footnote")
        st.write(f"Agents Involved: {agent_fn['agents_involved']}")
        st.write(f"Datasets Analyzed: {agent_fn['datasets_analyzed']}")
        st.write(f"Population Context: {agent_fn['population_context']}")
        st.dataframe(pd.DataFrame(agent_fn["agent_details"]))