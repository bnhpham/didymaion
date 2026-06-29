import requests
import streamlit as st

st.set_page_config(page_title="Didymaion", layout="wide")
st.title("Didymaion")
st.subheader("Your Market Intelligence Assistant")

query = st.text_area("Business question",
                     value="Should an EU electric vehicle manufacturer worry about copper availability over the next six months?"
                    )

if st.button("Run analysis"):

    with st.spinner("Running analysis..."):

        response = requests.post(
            "http://127.0.0.1:8000/analyze-query",
            json={"query": query},
            timeout=300
            )

    if response.status_code == 200:
        data = response.json()

        st.markdown("## Report")
        st.markdown(data["report"])

    else:
        st.error(f"Error: {response.status_code}")
        st.text(response.text)