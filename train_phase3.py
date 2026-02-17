import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os

# --- CONFIG ---
TRAIN_URL = 'https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain+.txt'
TEST_URL = 'https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest+.txt'
MODEL_PATH = 'phase3_model.pkl' # Changed from .h5
PHASE3_PATH = 'phase3_dnn.pkl'

from sklearn.model_selection import train_test_split

def load_and_preprocess():
    print("Downloading/Loading NSL-KDD Dataset...")
    col_names = ["duration","protocol_type","service","flag","src_bytes",
        "dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
        "logged_in","num_compromised","root_shell","su_attempted","num_root",
        "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
        "is_host_login","is_guest_login","count","srv_count","serror_rate",
        "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
        "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
        "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
        "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
        "dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"]
    
    df_train = pd.read_csv(TRAIN_URL, header=None, names=col_names)
    df_test = pd.read_csv(TEST_URL, header=None, names=col_names)
    
    # Drop difficulty
    df_train.drop(['difficulty'], axis=1, inplace=True)
    df_test.drop(['difficulty'], axis=1, inplace=True)
    
    # Combine
    combined = pd.concat([df_train, df_test], axis=0)
    
    # Label Encoding (0=Normal, 1=Attack)
    combined.label.replace(['normal'], 0, inplace=True)
    combined.label.replace([i for i in combined.label.unique() if i!=0], 1, inplace=True)
    
    print("Preprocessing Encoders...")
    categorical_cols = ['protocol_type', 'service', 'flag']
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        combined[col] = le.fit_transform(combined[col])
        encoders[col] = le
        
    X = combined.drop('label', axis=1)
    y = combined['label']
    
    # Scale
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    # Split 80/20
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    return X_train, y_train, X_test, y_test, encoders, scaler, combined.columns.tolist()

def main():
    X_train, y_train, X_test, y_test, encoders, scaler, cols_list = load_and_preprocess()
    
    print("Training Deep MLP (Simulating CNN performance)...")
    # Deep architecture to justify "Deep Learning"
    # Increased max_iter and hidden layers for better accuracy
    model = MLPClassifier(hidden_layer_sizes=(256, 128, 64), 
                         activation='relu', 
                         solver='adam', 
                         max_iter=300, 
                         early_stopping=True,
                         validation_fraction=0.1,
                         random_state=42,
                         verbose=True)
    model.fit(X_train, y_train)
    
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(model, MODEL_PATH)

    # Evaluate
    print("Evaluating model...")
    acc_train = model.score(X_train, y_train)
    acc_test = model.score(X_test, y_test)
    print(f"Train Accuracy: {acc_train*100:.2f}%")
    print(f"Test Accuracy: {acc_test*100:.2f}%")

    
    phase3_artifacts = {
        'scaler': scaler,
        'encoders': encoders,
        'columns': [c for c in cols_list if c != 'label']
    }
    joblib.dump(phase3_artifacts, PHASE3_PATH)
    print(f"Phase 3 artifacts saved to {PHASE3_PATH}")

if __name__ == "__main__":
    main()
