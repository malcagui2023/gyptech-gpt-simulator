import streamlit as st
import plotly.graph_objects as go
from PIL import Image

# Branding
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Gyptech_Logo.png/600px-Gyptech_Logo.png", width=200)

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
    "safety stock": {
        "reply": "To calculate safety stock: **SS = Z × σ × √L**",
        "note": "Refer to InventoryPolicy.pdf, Section 4.2."
    },
    "inventario": {
        "reply": "Para calcular el stock de seguridad: **SS = Z × σ × √L**",
        "note": "Ver la política de inventario, Sección 4.2."
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
if user_input:
    response = get_gpt_response(user_input)
    st.markdown(f"**Gyptech GPT:** {response['reply']}")

    if "breakdown" in response:
        with st.expander("📊 View Cost Breakdown"):
            st.write(response["breakdown"])

        # Main bar chart
        fig = go.Figure(data=[
            go.Bar(name='Cost', x=list(response["breakdown"].keys()), y=list(response["breakdown"].values()))
        ])
        fig.update_layout(title="Project 123 Cost Breakdown", yaxis_title="USD")
        st.plotly_chart(fig)

        # Line chart as second visualization
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=["Jan", "Feb", "Mar"], y=[100000, 200000, 350000], mode='lines+markers'))
        fig2.update_layout(title="Cost Accumulation Over Time", xaxis_title="Month", yaxis_title="USD")
        st.plotly_chart(fig2)

    if "pdf_link" in response:
        st.markdown(f"[📄 View Report PDF]({response['pdf_link']})")

    if "note" in response:
        st.info(response["note"])
else:
    st.info("Start by asking a question like:\n- What’s the cost of Project 123?\n- How do I calculate safety stock?\n- ¿Cómo se calcula el stock de seguridad?")
