import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Developer Onboarding Assistant",
    layout="wide"
)

st.title("Developer Onboarding Assistant")

# Backend Health Check
backend_online = True

try:
    response = requests.get(f"{API_URL}/health", timeout=2)
    if response.status_code != 200:
        backend_online = False
except requests.exceptions.RequestException:
    backend_online = False

if not backend_online:
    st.error(
        "Cannot connect to FastAPI backend. "
        "Please ensure the server is running on port 8000."
    )

# Layout
left, right = st.columns([1, 3])

# -------------------------
# Left Panel - Documents
# -------------------------
with left:
    st.subheader("Documents")

    uploaded_file = st.file_uploader(
        "Upload project documents",
        type=["pdf", "txt", "md"]
    )

    if uploaded_file:
        st.success(uploaded_file.name)

        if st.button("Index Document/ Upload Document", use_container_width=True):
            if backend_online:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                try:
                    progress = st.progress(0)

                    progress.progress(20)

                    response = requests.post(
                        f"{API_URL}/upload",
                        files=files,
                        timeout=120
                    )

                    progress.progress(100)

                    if response.status_code == 200:
                        data = response.json()

                        st.info(
                            f"Indexed {data['chunks']} chunks"
                        )
                    else:
                        st.error(response.text)

                except Exception as e:
                    st.error(str(e))

# -------------------------
# Right Panel - Chat
# -------------------------
with right:
    st.subheader("Chat")

    question = st.text_input(
        "Ask a question about your documents"
    )

    if st.button("Ask"):
        if backend_online:
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question},
                    timeout=120
                )

                if response.status_code == 200:
                    result = response.json()

                    st.markdown("### Answer")
                    st.write(result["answer"])

                    st.markdown("### Sources")

                    for source in result["sources"]:
                        st.write(f"- {source}")

                else:
                    st.error(response.text)

            except Exception as e:
                st.error(str(e))