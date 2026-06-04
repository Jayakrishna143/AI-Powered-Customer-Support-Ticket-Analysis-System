import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Customer Support Ticket Analyzer")
st.caption("Powered by Gemini AI")

st.subheader("Enter a support message")
message = st.text_area("Customer message", placeholder="e.g. I was charged twice and need a refund.", height=120)

if st.button("Analyze", type="primary"):
    if not message.strip():
        st.warning("Please enter a message first.")
    else:
        with st.spinner("Analyzing..."):
            try:
                res = requests.post(f"{API_URL}/analyze", json={"message": message})
                res.raise_for_status()
                data = res.json()

                col1, col2, col3 = st.columns(3)
                col1.metric("Category", data["category"])
                col2.metric("Priority", data["priority"])
                col3.metric("Escalation", data["escalation"])

                st.subheader("Extracted Details")
                for detail in data["extracted_details"]:
                    st.write(f"- {detail}")

                st.subheader("Suggested Response Draft")
                st.info(data["response_draft"])

            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.divider()

# ---------------------------------------------------------------------------
# Download Excel button
# ---------------------------------------------------------------------------
st.subheader("📥 Export Analysis History")
if st.button("Download Excel Report"):
    try:
        excel_res = requests.get(f"{API_URL}/export-excel")
        excel_res.raise_for_status()
        st.download_button(
            label="💾 Click here to save the file",
            data=excel_res.content,
            file_name="ticket_analysis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as e:
        st.error(f"Could not fetch the report: {e}")

st.divider()
st.subheader("Sample Messages")
st.caption("Copy any of these into the input box above.")
for msg in [
    "I was charged twice for my subscription and need a refund.",
    "My account got hacked and I can't log in anymore.",
    "How do I change my email address in settings?",
    "The app keeps crashing every time I open it on iPhone.",
    "I cancelled my plan but still got charged this month.",
    "I need to download an invoice for my company records.",
    "My data was deleted after the update. I need it restored immediately.",
    "Can you explain the difference between Pro and Basic plans?",
]:
    st.write(f"- {msg}")
