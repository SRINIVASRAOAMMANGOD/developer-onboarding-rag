import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Developer Onboarding Assistant")
st.title("Developer Onboarding Assistant")

# Check if the FastAPI backend is running
backend_online = True
try:
    health_response = requests.get(f"{API_URL}/health", timeout=2)
    if health_response.status_code != 200:
        backend_online = False
except requests.exceptions.RequestException:
    backend_online = False

if not backend_online:
    st.error("⚠️ Connection Error: Cannot connect to the FastAPI backend. Please verify that the backend is running at http://127.0.0.1:8000")

uploaded_file = st.file_uploader("Upload project docs", type=["pdf", "txt", "md"])

if uploaded_file and st.button("Index document"):
    if not backend_online:
        st.error("Cannot upload; backend server is offline.")
    else:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        try:
            response = requests.post(f"{API_URL}/upload", files=files, timeout=120)
            if response.status_code == 200:
                st.write(response.json())
            else:
                st.error(f"Error from backend: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to communicate with backend: {e}")

question = st.text_input("Ask a question")

if question and st.button("Ask"):
    if not backend_online:
        st.error("Cannot ask question; backend server is offline.")
    else:
        try:
            response = requests.post(f"{API_URL}/ask", json={"question": question}, timeout=120)
            if response.status_code == 200:
                result = response.json()
                st.subheader("Answer")
                st.write(result.get("answer", "No answer returned."))

                st.subheader("Citations")
                for source in result.get("sources", []):
                    st.write(f"- {source}")
            else:
                st.error(f"Error from backend: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to communicate with backend: {e}")

