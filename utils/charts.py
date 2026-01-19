import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# -------------------------------------------------------------------
# ADMIN CHARTS
# -------------------------------------------------------------------

def risk_distribution_chart(data: dict):
    """
    Pie chart showing population risk distribution.
    Expected data: dict like {"high": 19, "medium": 40, "low": 41}
    """
    if not data:
        return go.Figure()

    df = pd.DataFrame(list(data.items()), columns=['Risk Level', 'Percentage'])
    fig = px.pie(
        df,
        names="Risk Level",
        values="Percentage",
        hole=0.4,
        color="Risk Level",
        color_discrete_map={'high': 'orange', 'medium': 'yellow', 'low': 'green'}
    )

    fig.update_layout(
        title="Population Risk Distribution",
        legend_title="Risk Level",
        margin=dict(t=50, b=20, l=20, r=20)
    )

    return fig


def risk_age_chart(data: dict):
    """
    Bar chart showing high-risk percentage by age band.
    Expected data: dict or df with 'Age Band' and 'High Risk %'
    """
    if not data:
        return go.Figure()

    if isinstance(data, dict):
        df = pd.DataFrame(list(data.items()), columns=['Age Band', 'High Risk %'])
    else:
        df = data

    fig = px.bar(
        df,
        x="Age Band",
        y="High Risk %",
        text="High Risk %",
        color="High Risk %",
        color_continuous_scale="RdYlGn_r"
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        title="High-Risk Percentage by Age Band",
        yaxis_title="High-Risk (%)",
        xaxis_title="Age Band",
        margin=dict(t=50, b=40, l=40, r=20)
    )

    return fig


def cost_treemap_chart(labels: list, values: list):
    """
    Treemap for cost breakdown.
    Expected: lists of labels and values
    """
    if not labels or not values:
        return go.Figure()

    fig = px.treemap(
        names=labels,
        parents=[""] * len(labels),  # Flat treemap
        values=values,
        color=values,
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        title="Cost Breakdown by Category",
        margin=dict(t=50, b=20, l=20, r=20)
    )

    return fig


def equity_heatmap_chart(disparities: str):
    """
    Heatmap for equity disparities (simplified from description).
    Uses sample data; adapt as needed.
    """
    # Sample data based on disparities insight
    df = pd.DataFrame({
        'Cohort': ['Urban', 'Hispanic', 'Other'],
        'Instability Factor': [1.5, 1.5, 1.0]
    })

    fig = px.imshow(
        df.pivot(columns='Cohort', values='Instability Factor'),
        text_auto=True,
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        title="Equity Disparities Heatmap",
        margin=dict(t=50, b=40, l=40, r=20)
    )

    return fig


def care_flow_sankey():
    """
    Sankey diagram for care coordination flows (hardcoded sample).
    """
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=25,
            line=dict(color="black", width=0.5),
            label=["Primary Care", "Specialist", "Emergency", "Follow-up"],
            color=["#2B60DE", "#6495ED", "#FF6347", "#3CB371"]  # Professional color palette
        ),
        link=dict(
            source=[0, 1, 0, 2],  # From nodes
            target=[2, 3, 2, 3],  # To nodes
            value=[8, 4, 2, 2],
            color="rgba(200, 200, 200, 0.4)"  # Lighter, semi-transparent links
        )
    )])

    fig.update_layout(
        title_text="Care Flow Sankey Diagram",
        font=dict(size=12, color="black"),  # Improved font size and color
        margin=dict(t=50, b=20, l=20, r=20)
    )
    return fig


def hospitalization_scatter(data: dict):
    """
    Scatter plot for hospitalization risk vs age/condition.
    Expected: dict like hospitalization_risk_distribution
    """
    if not data:
        return go.Figure()

    # Sample expansion
    df = pd.DataFrame({
        'Risk': [0.2] * 50 + [0.5] * 30 + [0.8] * 20,
        'Age': list(range(20, 70)) * 2  # Simulated
    })

    fig = px.scatter(
        df,
        x="Age",
        y="Risk",
        title="Hospitalization Risk vs Age"
    )

    fig.update_layout(
        xaxis_title="Age",
        yaxis_title="Risk Score",
        margin=dict(t=50, b=40, l=40, r=20)
    )

    return fig


# -------------------------------------------------------------------
# DOCTOR CHARTS
# -------------------------------------------------------------------

def patient_risk_gauge(risk_score: float):
    """
    Gauge chart for individual patient risk.
    risk_score expected between 0 and 1.
    """
    risk_score = max(0, min(1, risk_score))

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        number={"suffix": ""},
        gauge={
            "axis": {"range": [0, 1]},
            "bar": {"thickness": 0.25},
            "steps": [
                {"range": [0, 0.4], "color": "#2ecc71"},
                {"range": [0.4, 0.7], "color": "#f1c40f"},
                {"range": [0.7, 1.0], "color": "#e74c3c"},
            ],
            "threshold": {
                "line": {"color": "black", "width": 2},
                "thickness": 0.75,
                "value": risk_score,
            },
        }
    ))

    fig.update_layout(
        title="Patient Risk Score",
        margin=dict(t=60, b=20, l=20, r=20),
        height=300
    )

    return fig


def encounter_timeline_chart(df: pd.DataFrame):
    """
    Timeline chart of patient encounters.
    Expected columns: ['Date', 'Type']
    """
    if df.empty:
        return go.Figure()

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    fig = px.scatter(
        df,
        x="Date",
        y="Type",
        color="Type",
        symbol="Type",
        size_max=10
    )

    fig.update_layout(
        title="Encounter Timeline",
        xaxis_title="Date",
        yaxis_title="Encounter Type",
        showlegend=False,
        margin=dict(t=50, b=40, l=40, r=20)
    )

    return fig