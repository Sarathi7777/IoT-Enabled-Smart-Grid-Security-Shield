import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import utils
import os

st.set_page_config(page_title="Forensics", page_icon="📄", layout="wide")

st.title("📄 Automated Forensic Reporting")
st.markdown("Generate comprehensive security reports for audit and compliance.")

# Mock Data for Report (In real app, this comes from database/logs)
data = {
    'Timestamp': ['2023-10-01 10:00', '2023-10-01 10:05', '2023-10-01 10:12', '2023-10-01 10:45'],
    'Attack Type': ['DoS', 'Probe', 'Normal', 'DoS'],
    'Source IP': ['192.168.1.5', '10.0.0.4', '192.168.1.2', '192.168.1.9'],
    'Action Taken': ['Blocked', 'Blocked', 'Allowed', 'Blocked']
}
df_log = pd.DataFrame(data)

st.subheader("Recent Incident Logs")
st.dataframe(df_log, use_container_width=True)

def create_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Smart Grid Security - Forensic Report", ln=1, align='C')
    pdf.ln(10)
    
    # Summary
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Total Incidents: {len(dataframe)}", ln=1)
    pdf.cell(200, 10, txt=f"Attacks Blocked: {len(dataframe[dataframe['Action Taken']=='Blocked'])}", ln=1)
    pdf.ln(10)
    
    # Table Header
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, "Timestamp", 1)
    pdf.cell(40, 10, "Type", 1)
    pdf.cell(40, 10, "Action", 1)
    pdf.ln()
    
    # Rows
    pdf.set_font("Arial", size=10)
    for index, row in dataframe.iterrows():
        pdf.cell(50, 10, row['Timestamp'], 1)
        pdf.cell(40, 10, row['Attack Type'], 1)
        pdf.cell(40, 10, row['Action Taken'], 1)
        pdf.ln()
        
    file_path = "forensic_report.pdf"
    pdf.output(file_path)
    return file_path

if st.button("📄 Generate & Download Report"):
    with st.spinner("Generating PDF..."):
        pdf_path = create_pdf(df_log)
        
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF",
                data=f,
                file_name="Forensic_Report.pdf",
                mime="application/pdf"
            )
            
st.markdown("### Attack Distribution")
chart_data = df_log['Attack Type'].value_counts()
st.bar_chart(chart_data)
