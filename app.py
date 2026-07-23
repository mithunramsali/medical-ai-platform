import streamlit as st
import requests
from PIL import Image

st.set_page_config(
    page_title="Advanced AI Medical Intelligence Platform",
    page_icon="🏥",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

st.title("🏥 Advanced AI Medical Intelligence Platform")
st.markdown("### Explainable AI & LLM-Assisted Radiographic Diagnostic Suite")
st.markdown("---")

option = st.sidebar.radio("Navigation Menu", ["Diagnostic Workspace", "Prediction Audit Logs"])

if option == "Diagnostic Workspace":
    st.subheader("📤 Upload Radiographic Scan")
    uploaded_file = st.file_uploader("Select Chest X-Ray or Medical Scan...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col1, col2 = st.columns(2)

        image = Image.open(uploaded_file)
        with col1:
            st.image(image, caption="Original Input Scan", use_container_width=True)

        if st.sidebar.button("⚡ Run Diagnostic Analysis"):
            with st.spinner("Processing image through ResNet-18 Deep Learning & Grad-CAM Pipeline..."):
                try:
                    bytes_data = uploaded_file.getvalue()
                    files = {"file": (uploaded_file.name, bytes_data, uploaded_file.type)}
                    
                    response = requests.post(f"{API_URL}/predict", files=files)
                    
                    if response.status_code == 200:
                        res_data = response.json()
                        st.sidebar.success("Analysis Complete!")
                        
                        with col2:
                            cam_path = res_data["cam_image_path"]
                            st.image(cam_path, caption="Explainable AI (Grad-CAM Heatmap)", use_container_width=True)
                        
                        st.markdown("---")
                        st.subheader("📊 Diagnostic Summary & Confidence Metrics")
                        
                        m1, m2 = st.columns(2)
                        m1.metric("Predicted Classification", res_data["prediction"])
                        m2.metric("Confidence Score", f"{res_data['confidence'] * 100:.2f}%")
                        
                        st.markdown("---")
                        st.subheader("📝 Automated LLM Clinical Report")
                        st.info(res_data["report"])
                    else:
                        st.error(f"Error from API: {response.text}")
                
                except Exception as e:
                    st.error(f"Failed to connect to API backend: {e}")

elif option == "Prediction Audit Logs":
    st.subheader("📜 Database History Logs")
    if st.button("Refresh History"):
        try:
            res = requests.get(f"{API_URL}/history")
            if res.status_code == 200:
                history_data = res.json()
                st.dataframe(history_data, use_container_width=True)
            else:
                st.error("Failed to load audit logs.")
        except Exception as e:
            st.error(f"Connection error: {e}")