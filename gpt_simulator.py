import streamlit as st
import plotly.graph_objects as go

# App config
st.set_page_config(page_title="Gyptech GPT Simulator", layout="centered")
st.title("🤖 Gyptech GPT - Internal Assistant Simulator")

st.markdown("Ask a business question below and watch the AI assistant simulate a reply based on internal knowledge.")

# Simulated GPT response logic
def get_gpt_response(query):
    query = query.lower()
    if "project 123" in query:
        return {
            "reply": "The current cost incurred on Project 123 is **$350,000**.",
            "breakdown": {
                "Labor": 200000,
                "Materials": 150000
            },
            "pdf_link": "https://example.com/Project123_Report.pdf"
        }
    elif "safety stock" in query:
        return {
            "reply": "To calculate safety stock: **SS = Z × σ × √L**",
            "note": "Refer to InventoryPolicy.pdf, Section 4.2."
        }
    else:
        return {"reply": "❌ Sorry, I couldn't find data for that query."}

# Input section
user_input = st.text_input("Ask Gyptech GPT something...", "")

# Display result
if user_input:
    response = get_gpt_response(user_input)
    st.markdown(f"**Gyptech GPT:** {response['reply']}")

    if "breakdown" in response:
        with st.expander("📊 View Cost Breakdown"):
            st.write(response["breakdown"])

        fig = go.Figure(data=[
            go.Bar(name='Cost', x=list(response["breakdown"].keys()), y=list(response["breakdown"].values()))
        ])
        fig.update_layout(title="Project 123 Cost Breakdown", yaxis_title="USD")
        st.plotly_chart(fig)

    if "pdf_link" in response:
        st.markdown(f"[📄 View Report PDF]({response['pdf_link']})")

    if "note" in response:
        st.info(response["note"])
else:
    st.info("Start by asking a question like:\n- What’s the cost of Project 123?\n- How do I calculate safety stock?")
