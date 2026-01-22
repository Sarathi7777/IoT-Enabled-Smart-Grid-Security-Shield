import streamlit as st
import pandas as pd
import numpy as np
import time
import utils

st.set_page_config(page_title="Live Monitor", page_icon="📡", layout="wide")

# Load Systems
system = utils.load_system()
phase3 = utils.load_phase3_system()
cnn_model = utils.load_cnn_model()

if system is None:
    st.error("🚨 System initialization failed. Please Ensure 'smart_grid_security_system.pkl' is present.")
    st.stop()

rf_model = system['rf_model']
bpnn_model = system['bpnn_model']
scaler = system['scaler']
encoders = system['encoders']
columns = system['columns']

st.title("📡 Real-Time Traffic Monitor")
st.markdown("Simulate and analyze network traffic packets in real-time.")
st.divider()

col_control, col_display = st.columns([1, 2])

with col_control:
    st.subheader("🎮 Attack Simulation")
    st.info("Select a traffic pattern to trigger:")
    
    if st.button("🟢 Generate Normal Traffic", use_container_width=True):
        st.session_state['sim_type'] = 'normal'
        st.session_state['trigger'] = True
        
    if st.button("🔴 Simulate DoS Attack", use_container_width=True):
        st.session_state['sim_type'] = 'dos'
        st.session_state['trigger'] = True
        
    if st.button("🟠 Simulate Probe / Scan", use_container_width=True):
        st.session_state['sim_type'] = 'probe'
        st.session_state['trigger'] = True

    st.markdown("---")
    st.markdown("**Active Model:**")
    model_choice = st.radio("Detection Engine:", ["Hybrid RF-BPNN", "Deep Learning (1D-CNN)"])

with col_display:
    st.subheader("🔍 Inspection Result")
    
    if 'trigger' in st.session_state and st.session_state['trigger']:
        st.session_state['trigger'] = False
        sim_type = st.session_state.get('sim_type', 'normal')
        
        with st.spinner("Intercepting Packet & Analyzing..."):
            time.sleep(0.6) # Sim delay
            
            # --- PACKET GENERATION LOGIC ---
            # We construct a dataframe matching 'columns'
            # Note: columns includes 'label', we drop it for input
            input_cols = [c for c in columns if c != 'label' and c != 'difficulty']
            input_data = pd.DataFrame(0, index=[0], columns=input_cols)
            
            # Defaults for categorical
            p_type = 'tcp'
            svc = 'http'
            flg = 'SF'
            
            if sim_type == 'normal':
                # Normal-ish params
                src = np.random.randint(100, 500)
                dst = np.random.randint(200, 2000)
                b_cnt = np.random.randint(1, 10)
                sev_rate = 0.0
            elif sim_type == 'dos':
                # DoS: High count, small time, SYN flood (S0)
                p_type = 'tcp'
                flg = 'S0' # Connection attempt seen, no reply
                src = 0
                dst = 0
                b_cnt = np.random.randint(100, 300) # High count
                sev_rate = 1.0 # High error rate
            elif sim_type == 'probe':
                # Probe: Scanning ports
                p_type = 'icmp' # or tcp
                svc = 'eco_i' # Ping
                b_cnt = np.random.randint(1, 5)
                sev_rate = 0.0
                src = np.random.randint(10, 100)
                dst = 0
            
            # Helper to safe transform
            def safe_transform(enc_dict, col, val):
                try:
                    return enc_dict[col].transform([val])[0]
                except:
                    # Fallback to mode or 0 if unseen
                    return 0
            
            # Fill Data
            # Note: This requires 'encoders' to have these keys. 
            # If phase 3 encoders differ, we might need mapping. 
            # Assuming Phase 2 encoders for RF-BPNN and Phase 3 for CNN logic if different.
            # For simplicity, we use system['encoders'] for generation.
            
            input_data['protocol_type'] = safe_transform(encoders, 'protocol_type', p_type)
            input_data['service'] = safe_transform(encoders, 'service', svc)
            input_data['flag'] = safe_transform(encoders, 'flag', flg)
            input_data['src_bytes'] = src
            input_data['dst_bytes'] = dst
            input_data['count'] = b_cnt
            input_data['serror_rate'] = sev_rate
            
            # Add some noise to others
            input_data['same_srv_rate'] = np.random.random()
            
            # --- PREDICTION ---
            pred_label = 0
            conf = 0.0
            
            if model_choice == "Hybrid RF-BPNN":
                # RF-BPNN Pipeline
                input_scaled = scaler.transform(input_data)
                rf_prob = rf_model.predict_proba(input_scaled)[:, 1].reshape(-1, 1)
                hybrid_input = np.hstack((input_scaled, rf_prob))
                pred_label = bpnn_model.predict(hybrid_input)[0]
                conf = bpnn_model.predict_proba(hybrid_input).max() * 100
                
            else: # Deep Learning
                if cnn_model is None:
                    st.error("Deep Model not loaded. Switch to Hybrid.")
                else:
                    if phase3:
                        p3_scaler = phase3['scaler']
                        input_scaled = p3_scaler.transform(input_data)
                    else:
                        input_scaled = scaler.transform(input_data)
                        
                    # MLP Prediction (No Reshape needed)
                    prob = cnn_model.predict_proba(input_scaled)[0][1]
                    pred_label = 1 if prob > 0.5 else 0
                    conf = prob * 100 if pred_label == 1 else (1-prob)*100

            # --- DISPLAY ---
            st.write(f"**Packet Summary:** {p_type.upper()} | {svc} | {flg} | Count: {b_cnt}")
            
            if pred_label == 1:
                st.error(f"🚨 **ATTACK DETECTED** ({sim_type.upper()} Simulation)")
                st.metric("Threat Confidence", f"{conf:.2f}%")
                st.toast(f"⚠️ Alert: {sim_type.upper()} Attack Blocked!", icon="🔥")
                
                # Log event (Mock)
                with open("attack_log.txt", "a") as f:
                    f.write(f"{time.ctime()} | {sim_type} | Blocked\n")
            else:
                st.success(f"✅ **NORMAL TRAFFIC**")
                st.metric("Safety Score", f"{conf:.2f}%")
                
    else:
        st.info("Waiting for simulation trigger...")

