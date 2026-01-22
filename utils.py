import streamlit as st
import joblib
import os

@st.cache_resource
def load_system():
    """Loads the Phase 2 system (RF/BPNN)"""
    if os.path.exists('smart_grid_security_system.pkl'):
        return joblib.load('smart_grid_security_system.pkl')
    return None

@st.cache_resource
def load_phase3_system():
    """Loads Phase 3 artifacts (Scaler/Encoders for CNN)"""
    if os.path.exists('phase3_dnn.pkl'):
        return joblib.load('phase3_dnn.pkl')
    return None

@st.cache_resource
def load_cnn_model():
    """Loads the trained Deep Model (MLP/CNN)"""
    # Using 'phase3_model.pkl' now instead of h5
    if os.path.exists('phase3_model.pkl'):
        return joblib.load('phase3_model.pkl')
    return None
