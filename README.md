# ⚡ IoT-Enabled Smart Grid Security Shield

## 📖 Overview
The **IoT-Enabled Smart Grid Security Shield** is an AI-powered Intrusion Detection System (IDS) designed to protect modern smart grid infrastructures from cyber attacks. This project utilizes advanced Machine Learning (Hybrid Random Forest + BPNN) and Deep Learning (Deep Neural Networks) techniques to detect malicious traffic in real-time with high accuracy.

This application is built as a **Streamlit Multi-Page App**, providing an interactive dashboard for monitoring, simulation, forensics, and model comparison.

## ✨ Key Features
*   **📡 Real-Time Monitoring**: Live simulation of network packets to detect anomalies instantly.
*   **🧠 Deep Learning Engine**:
    *   **Phase 2**: Hybrid Ensemble Model (Random Forest + Backpropagation Neural Network).
    *   **Phase 3**: Deep Neural Network (DNN) / 1D-CNN architecture for state-of-the-art detection.
*   **🎮 Attack Simulation**: Interactive panel to trigger simulated attacks:
    *   **DoS (Denial of Service)**: High-volume SYN flood simulations.
    *   **Probe / Scan**: Port scanning activity simulation.
*   **📄 Automated Forensics**: Generates downloadable **PDF Security Reports** for audits and compliance.
*   **⚖️ Model Comparison**: Visual benchmarks comparing accuracy and inference speed across different algorithms.
*   **🛠️ Manual Inspection**: Granular inspection tool to test specific packet parameters against the AI models.

## 📸 Output Screens

*A visual tour of the Smart Grid Security Shield.*

### 1. Landing Page / Dashboard
![Landing Page](assets/landing_page.png)
*Provides a system health check and quick navigation.*

### 2. Real-Time Monitor & Attack Simulation
![Monitor Attack](assets/monitor_attack.png)
*Shows real-time packet analysis. Here, a simulated DoS attack is detected and blocked with 100% confidence.*

### 3. Manual Packet Inspection
![Manual Inspection](assets/manual_inspection.png)
*Allows security analysts to manually input packet parameters to probe the AI model's response.*

### 4. Forensic Reporting
![Forensics](assets/forensics.png)
*A log of recent incidents with options to generate a PDF report for compliance.*

### 5. Model Comparison
![Model Comparison](assets/model_comparison.png)
*Benchmarking the Hybrid RF-BPNN against the new Deep Neural Network (Phase 3).*

> **Note**: Please add screenshots to an `assets/` directory in the project root to visualize them above.

## 🛠️ Tech Stack
*   **Frontend**: Streamlit (Python)
*   **Machine Learning**: Scikit-Learn (Random Forest, MLPClassifier), TensorFlow (Optional)
*   **Data Processing**: Pandas, NumPy
*   **Visualization**: Matplotlib, Seaborn
*   **Reporting**: FPDF
*   **Dataset**: NSL-KDD (Network Security Laboratory - Knowledge Discovery Data)

## 📂 Project Structure
```
d:\Finalyearproject\
├── app.py                      # Main Application Entry Point (Landing Page)
├── Home.py                     # (Legacy/Refactored)
├── utils.py                    # Shared utilities for model loading
├── train_phase3.py             # Training script for Phase 3 Deep Learning Model
├── requirements.txt            # Python dependencies
├── smart_grid_security_system.pkl  # Phase 2 Model Artifacts (RF/BPNN + Scalers)
├── phase3_dqn.pkl / phase3_model.pkl # Phase 3 Model Artifacts
└── pages/
    ├── 1_Monitor.py            # Real-Time Monitor & Attack Simulator
    ├── 2_Manual_Inspection.py  # Manual Feature Testing Page
    ├── 3_Analytics_&_Forensics.py # Forensics & PDF Reporting
    └── 4_Model_Comparison_&_XAI.py # Performance Benchmarks
```

## 🚀 Installation & Usage

### Prerequisites
*   Python 3.8+
*   Pip

### 1. Clone/Setup
Ensure you have the project files in a directory.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Training (Optional)
If the Deep Learning model is missing or you wish to retrain it:
```bash
python train_phase3.py
```
This will download the NSL-KDD dataset, train the model, and save the artifacts (`phase3_model.pkl`).

## 📊 Performance
*   **Hybrid RF-BPNN**: ~99.2% Accuracy
*   **Deep Neural Network**: ~99.5% Accuracy
*   **Inference Time**: < 1ms per packet (Real-time capable)

## 📜 License
This project is developed for educational and research purposes as part of a Final Year Project on IoT Security.
