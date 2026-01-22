import streamlit as st
import utils

st.set_page_config(
    page_title="IoT Shield - Smart Grid Security",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ IoT-Enabled Smart Grid Security Shield")
st.markdown("### AI-Powered Intrusion Detection System (IDS)")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    **Welcome to the Security Console.**
    
    This system protects IoT-enabled Smart Grids from cyber attacks using Advanced Machine Learning and Deep Learning.
    
    #### 🚀 Core Features (Phase 3 Enriched):
    - **Live Monitoring**: Real-time packet analysis & attack simulation.
    - **Deep Learning**: 1D-CNN Integration for high-accuracy detection.
    - **Forensics**: Automated PDF Reporting for security audits.
    - **Adversarial Simulation**: Test system robustness against DoS & Probing.
    - **XAI**: Model Comparison & Explainability.
    
    **Get Started:** Use the sidebar to navigate to the **Monitor** or **Analytics**.
    """)

with col2:
    st.info("System Status Check")
    
    # Check Phase 2 System
    sys = utils.load_system()
    if sys:
        st.success("✅ Hybrid RF-BPNN Model: ONLINE")
    else:
        st.error("❌ Hybrid Model: OFFLINE (Missing pickle)")
        
    # Check Phase 3 System
    cnn = utils.load_cnn_model()
    if cnn:
        st.success("✅ Deep Learning (DNN): ONLINE")
    else:
        st.warning("⚠️ Deep Learning: INITIALIZING... (Run Training)")
    
    st.markdown("---")
    st.caption("Final Year Project | Phase 3 Implementation")
