import streamlit as st
import plotly.graph_objects as go
import math
import pandas as pd

# Branding
st.set_page_config(page_title="Gyptech GPT", page_icon="🤖", layout="centered")
st.image("SCM-Analytics Logo.jfif", width=200)

# App Header
st.title("Gyptech GPT – Internal AI Assistant")
st.markdown("Ask common business questions and get simulated AI-powered responses from your internal knowledge base.")

# Simulated GPT response logic with smarter matching
responses = {
    "project 123": {
        "reply": "The current cost incurred on Project 123 is **$350,000**.",
        "breakdown": {
            "Labor": 200000,
            "Materials": 150000
        },
        "pdf_link": "https://example.com/Project123_Report.pdf"
    },
    "safety stock for product abc": {
        "reply": "To calculate safety stock for product ABC, we use the following parameters:\n\n- Z-score (95% service level): **1.65**\n- Standard deviation of demand (σ): **120 units**\n- Lead time: **7 days**\n\nEstimated Safety Stock = 1.65 × 120 × √7 ≈ **525 units**",
        "note": "Values are based on past 3 months of demand data and current supplier lead time."
    },
    "inventario": {
        "reply": "Para calcular el stock de seguridad: **SS = Z × σ × √L**",
        "note": "Ver la política de inventario, Sección 4.2."
    },
    "calculate safety stock manually": {
        "reply": "Sure! Please enter your own values for Z-score, standard deviation of demand, and lead time below."
    },
    "historical demand": {
        "reply": "Here's the historical monthly demand for product ABC over the last 6 months."
    }
}

# NLP-style soft match
def get_gpt_response(query):
    query = query.lower()
    for keyword, response in responses.items():
        if keyword in query:
            return response
    return {"reply": "❌ Sorry, I couldn't find data for that query."}

# Input section
user_input = st.text_input("Ask Gyptech GPT something...", "")

# Display result
show_calculator = False
show_historical_demand = False
calculated_safety_stock = None

if user_input:
    response = get_gpt_response(user_input)
    st.markdown(f"**Gyptech GPT:** {response['reply']}")

    if user_input.lower() == "calculate safety stock manually":
        show_calculator = True

    if user_input.lower() == "historical demand":
        show_historical_demand = True

    if "breakdown" in response:
        with st.expander("📊 View Cost Breakdown"):
            st.write(response["breakdown"])

        fig = go.Figure(data=[
            go.Bar(name='Cost', x=list(response["breakdown"].keys()), y=list(response["breakdown"].values()))
        ])
        fig.update_layout(title="Project 123 Cost Breakdown", yaxis_title="USD")
        st.plotly_chart(fig)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=["Jan", "Feb", "Mar"], y=[100000, 200000, 350000], mode='lines+markers'))
        fig2.update_layout(title="Cost Accumulation Over Time", xaxis_title="Month", yaxis_title="USD")
        st.plotly_chart(fig2)

    if "pdf_link" in response:
        st.markdown(f"[📄 View Report PDF]({response['pdf_link']})")

    if "note" in response:
        st.info(response["note"])

# Dynamic Safety Stock Calculator
if show_calculator:
    st.markdown("---")
    st.subheader("🧮 Safety Stock Calculator")

    with st.expander("ℹ️ Explanation of Parameters"):
        st.markdown("**Z-score**: Measures the desired service level. A Z-score of 1.65 represents a 95% confidence level that stock will meet demand.")
        st.markdown("**Standard Deviation of Demand (σ)**: Measures the variability of demand. Higher values mean demand is less predictable.")
        st.markdown("**Lead Time (days)**: The number of days between placing and receiving a replenishment order.")

    z = st.number_input("Z-score (e.g., 1.65 for 95% service level)", min_value=0.0, value=1.65)
    sigma = st.number_input("Standard deviation of demand (σ)", min_value=0.0, value=100.0)
    lead_time = st.number_input("Lead time (days)", min_value=0.0, value=5.0)

    if st.button("Calculate Safety Stock"):
        calculated_safety_stock = round(z * sigma * math.sqrt(lead_time))
        st.success(f"Estimated Safety Stock: **{calculated_safety_stock} units**")

        # Export button
        csv_data = pd.DataFrame({
            "Z-score": [z],
            "Std Dev (σ)": [sigma],
            "Lead Time (days)": [lead_time],
            "Safety Stock": [calculated_safety_stock]
        })
        st.download_button("📥 Download Results as CSV", csv_data.to_csv(index=False), file_name="safety_stock_result.csv")

# Historical demand chart
if show_historical_demand:
    st.markdown("---")
    st.subheader("📈 Historical Demand – Product ABC")

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    volumes = [320, 410, 390, 450, 470, 430]
    df_hist = pd.DataFrame({"Month": months, "Units Sold": volumes})

    fig = go.Figure([go.Bar(x=months, y=volumes)])
    fig.update_layout(title="Monthly Demand for Product ABC", xaxis_title="Month", yaxis_title="Units")
    st.plotly_chart(fig)

    st.dataframe(df_hist)
    st.download_button("📥 Download Demand Data", df_hist.to_csv(index=False), file_name="historical_demand_abc.csv")

else:
    st.info("Start by asking a question like:\n- What’s the cost of Project 123?\n- How do I calculate safety stock for product ABC?\n- Calculate safety stock manually\n- Historical demand\n- ¿Cómo se calcula el stock de seguridad?")
