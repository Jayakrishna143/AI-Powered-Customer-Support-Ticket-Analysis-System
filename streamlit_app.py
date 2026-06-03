import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Customer Support Ticket Analyzer")
st.caption("Powered by Claude AI")

tab1, tab2 = st.tabs(["Analyze Ticket", "Sample Dataset"])

with tab1:
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

with tab2:
    st.subheader("Sample Dataset")
    st.caption("These messages were used to design and test the system.")
    try:
        res = requests.get(f"{API_URL}/dataset")
        res.raise_for_status()
        dataset = res.json()

        for item in dataset:
            with st.expander(item["message"][:60] + "..."):
                st.write(f"**Category:** {item['category']}")
                st.write(f"**Priority:** {item['priority']}")
                if st.button("Analyze this", key=item["message"]):
                    with st.spinner("Analyzing..."):
                        r = requests.post(f"{API_URL}/analyze", json={"message": item["message"]})
                        d = r.json()
                        st.write(f"**Extracted Details:** {', '.join(d['extracted_details'])}")
                        st.write(f"**Escalation:** {d['escalation']}")
                        st.info(d["response_draft"])
    except Exception as e:
        st.error(f"Could not load dataset: {e}")
