import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Mitigation Action Center", page_icon="🛡️", layout="wide")

st.title("🛡️ Mitigation Action Center")
st.markdown("---")

# Mock Incidents
if "incidents" not in st.session_state:
    st.session_state.incidents = [
        {"id": "INC-001", "type": "DoS Attack", "source": "192.168.1.105", "severity": "High", "status": "Active"},
        {"id": "INC-002", "type": "Probe", "source": "10.0.0.45", "severity": "Medium", "status": "Active"},
        {"id": "INC-003", "type": "U2R (User to Root)", "source": "172.16.0.12", "severity": "Critical", "status": "Pending Analysis"},
    ]

# Display Statistics
active_count = len([i for i in st.session_state.incidents if i['status'] in ['Active', 'Pending Analysis']])
mitigated_count = len([i for i in st.session_state.incidents if i['status'] == 'Mitigated'])

col1, col2 = st.columns(2)
col1.metric("Active Incidents", active_count, delta=active_count, delta_color="inverse")
col2.metric("Mitigated Threats", mitigated_count, delta=mitigated_count)

st.divider()

st.subheader("⚠️ Active Threats Checklist")

# Interactive Incident List
for index, incident in enumerate(st.session_state.incidents):
    if incident['status'] != 'Mitigated':
        with st.container():
            c1, c2, c3, c4, c5 = st.columns([1, 2, 2, 2, 2])
            c1.markdown(f"**{incident['id']}**")
            c2.markdown(f"**Type:** {incident['type']}")
            c3.markdown(f"**Source:** {incident['source']}")
            c4.markdown(f"**Severity:** {incident['severity']}")
            
            # Action Buttons
            if c5.button("Block IP & Quarantine", key=f"block_{index}"):
                with st.spinner("Applying firewall rules..."):
                    time.sleep(1.5) # Simulate API call
                incident['status'] = 'Mitigated'
                st.success(f"Threat {incident['id']} from {incident['source']} has been BLOCKED.")
                st.rerun()

st.divider()

st.subheader("✅ Mitigated Incidents Log")
mitigated_df = pd.DataFrame([i for i in st.session_state.incidents if i['status'] == 'Mitigated'])
if not mitigated_df.empty:
    st.dataframe(mitigated_df, use_container_width=True)
else:
    st.info("No mitigated incidents yet.")

# Playbook Section
with st.expander("📖 Security Playbook (Reference)"):
    st.markdown("""
    ### Defense Strategies
    1.  **DoS/DDoS**:
        -   Rate Limiting (limit requests/sec from single IP).
        -   IP Blacklisting.
        -   Traffic Scrubbing services.
    2.  **Probe/Port Scan**:
        -   Implement IDS/IPS rules to drop scanning packets.
        -   Hide open ports (Port Knocking).
    3.  **U2R/R2L**:
        -   Patch vulnerabilities immediately.
        -   Enforce complex passwords and 2FA.
        -   Isolate compromised hosts.
    """)
