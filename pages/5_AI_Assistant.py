import streamlit as st
import time
import google.generativeai as genai

# Page config
st.set_page_config(page_title="AI Security Assistant", page_icon="🤖", layout="wide")

st.title("🤖 AI Security Assistant")
st.markdown("---")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Gemini API Key", type="password", help="Get your key from Google AI Studio")
    st.info("Ensure you have an active internet connection.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def get_gemini_response(prompt, api_key):
    if not api_key:
        return "⚠️ Please enter your Gemini API Key in the sidebar to proceed."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # System Context (Implicitly added to prompt for now, or use chat history)
        # System Context (Project-Aware)
        system_context = """
        You are an expert Cybersecurity Analyst for the **"IoT-Enabled Smart Grid Security Shield"**, a cutting-edge Intrusion Detection System (IDS).

        **Your Roles:**
        1.  **Platform Expert:** You have deep knowledge of this specific application:
            *   **Core Engine:** Uses a **Hybrid RF-BPNN** model and a specialized **Deep Neural Network (MLP of 256-128-64)** achieving >99% accuracy.
            *   **Modules:** Real-time Monitor, Geolocation Threat Map, Manual Inspection, and Automated Forensics.
            *   **Capabilities:** Detects **DoS** (e.g., SYN Floods) and **Probe** (e.g., Port Scans) attacks in real-time.
        2.  **Security Advisor:** Explain network threats and suggest mitigations:
            *   **DoS:** Suggest rate limiting, traffic scrubbing, or using the **'Mitigation'** page to block IPs.
            *   **Probe:** Suggest IDS rules, hiding open ports, or checking the **'Threat Map'**.

        **Guidelines:**
        *   Keep answers **concise**, **professional**, and **actionable**.
        *   **Context Awareness:** You are integrated into the Streamlit dashboard.
        *   If asked about **"Current System Status"**, explain that you are an AI assistant and they should check the **'Monitor'** page for live data.
        *   If asked to **"Block an IP"**, guide them to the **'Mitigation Action Center'**.
        """
        
        full_prompt = f"{system_context}\n\nUser: {prompt}\nAnalyst:"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# React to user input
if prompt := st.chat_input("Ask about grid security, threats, or mitigation..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Analyzing..."):
            ai_response = get_gemini_response(prompt, api_key)
            
        # Simulate typing for better UX
        full_response = ""
        for chunk in ai_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
