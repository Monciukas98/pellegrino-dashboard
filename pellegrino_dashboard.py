import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Sample ESG data for Apple and competitors
esg_data = pd.DataFrame({
    "Company": ["Apple", "Apple", "Apple", "Microsoft", "Microsoft", "Microsoft",
                "Google", "Google", "Google", "Amazon", "Amazon", "Amazon"],
    "Category": ["Environmental", "Social", "Governance"] * 4,
    "Score": [32, 45, 38, 45, 50, 42, 40, 48, 41, 28, 35, 30]
})

# Function to assign ESG ratings
def get_esg_rating(score):
    if score <= 20:
        return "A+"
    elif score <= 30:
        return "A"
    elif score <= 40:
        return "B+"
    elif score <= 50:
        return "B"
    elif score <= 60:
        return "C+"
    elif score <= 70:
        return "C"
    elif score <= 80:
        return "D"
    else:
        return "F"

# Calculate total ESG score per company
total_scores = esg_data.groupby("Company")["Score"].mean()
esg_ratings = total_scores.apply(get_esg_rating)

total_scores = total_scores.to_frame().reset_index()
total_scores.columns = ["Company", "Total ESG Score"]
total_scores["ESG Rating"] = esg_ratings.values

# Streamlit App
st.title("🌍 Pellegrino Scoring Tool - ESG Ratings Dashboard")

# ESG Ratings Dashboard
st.subheader("📊 ESG Score Breakdown")
company_selected = st.selectbox("Select a Company", esg_data["Company"].unique())
filtered_data = esg_data[esg_data["Company"] == company_selected]
total_score_data = total_scores[total_scores["Company"] == company_selected]
st.metric(label="Total ESG Score", value=round(total_score_data["Total ESG Score"].iloc[0], 2))
st.metric(label="ESG Rating", value=total_score_data["ESG Rating"].iloc[0])

# Bar chart with distinct colors for ESG categories
fig = px.bar(
    filtered_data,
    x="Category",
    y="Score",
    color="Category",
    labels={"x": "ESG Category", "y": "Score (0-100)"},
    title=f"{company_selected} ESG Scores",
    color_discrete_map={"Environmental": "#C5DCA0", "Social": "#76C1BF", "Governance": "#508CA4"}
)
st.plotly_chart(fig)

# ESG Comparison with Other Companies
st.subheader("📊 ESG Comparison")
st.write("Compare the selected company's ESG scores against competitors.")
fig_comp = px.bar(
    esg_data,
    x="Company",
    y="Score",
    color="Category",
    title="ESG Comparison Across Companies",
    barmode="group",
    labels={"value": "Score (0-100)", "variable": "ESG Category"},
    color_discrete_map={"Environmental": "#C5DCA0", "Social": "#76C1BF", "Governance": "#508CA4"}
)
st.plotly_chart(fig_comp)