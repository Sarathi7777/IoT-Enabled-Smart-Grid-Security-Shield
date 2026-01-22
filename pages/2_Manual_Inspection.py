import streamlit as st
import pandas as pd
import numpy as np
import utils

st.set_page_config(page_title="Manual Inspection", page_icon="🛠️", layout="wide")

system = utils.load_system()
if not system:
    st.error("System missing.")
    st.stop()

rf_model = system['rf_model']
bpnn_model = system['bpnn_model']
scaler = system['scaler']
encoders = system['encoders']
columns = system['columns']

st.title("🛠️ Manual Packet Inspection")
st.markdown("Deep dive: Inspect specific packet parameters.")

with st.form("manual_form"):
    c1, c2, c3 = st.columns(3)
    
    with c1:
        p_type = st.selectbox("Protocol", encoders['protocol_type'].classes_)
        svc = st.selectbox("Service", encoders['service'].classes_)
        flg = st.selectbox("Flag", encoders['flag'].classes_)
        
    with c2:
        src = st.number_input("Src Bytes", 0, 100000, 200)
        dst = st.number_input("Dst Bytes", 0, 100000, 500)
        cnt = st.number_input("Count", 0, 500, 10)
        
    with c3:
        srv_rate = st.slider("Same Srv Rate", 0.0, 1.0, 0.5)
        diff_rate = st.slider("Diff Srv Rate", 0.0, 1.0, 0.0)
        
    submit = st.form_submit_button("🔍 Grade Packet")

if submit:
    # Construct DF
    input_cols = [c for c in columns if c != 'label' and c != 'difficulty']
    df = pd.DataFrame(0, index=[0], columns=input_cols)
    
    df['protocol_type'] = encoders['protocol_type'].transform([p_type])
    df['service'] = encoders['service'].transform([svc])
    df['flag'] = encoders['flag'].transform([flg])
    df['src_bytes'] = src
    df['dst_bytes'] = dst
    df['count'] = cnt
    df['same_srv_rate'] = srv_rate
    df['diff_srv_rate'] = diff_rate
    
    # Predict
    input_scaled = scaler.transform(df)
    rf_prob = rf_model.predict_proba(input_scaled)[:, 1].reshape(-1, 1)
    hybrid_input = np.hstack((input_scaled, rf_prob))
    pred = bpnn_model.predict(hybrid_input)[0]
    conf = bpnn_model.predict_proba(hybrid_input).max() * 100
    
    if pred == 1:
        st.error(f"🚨 MALICIOUS (Confidence: {conf:.2f}%)")
    else:
        st.success(f"✅ SAFE (Confidence: {conf:.2f}%)")
