import streamlit as st
import pennylane as qml
from pennylane import numpy as np


st.set_page_config(page_title="Quantum Wireless Manager", page_icon="📡")
st.title("📡 Quantum-AI Connection Manager")
st.write("This app uses a Quantum Neural Network to decide if a 6G client should be accepted or rejected based on signal quality.")


dev = qml.device("default.qubit", wires=1)

@qml.qnode(dev)
def quantum_brain(signal_strength, weight):
    # Encoding the signal
    qml.RY(signal_strength, wires=0)
    # The learned 'Ruleset'
    qml.RX(weight, wires=0)
    return qml.expval(qml.PauliZ(0))

# Pre-trained weight (In a real project, you'd train this first)
learned_weight = 1.57 

# --- USER INTERFACE (The Application) ---
st.sidebar.header("Client Input Simulation")
client_name = st.sidebar.text_input("Client Name", "Device_001")
signal_val = st.sidebar.slider("Signal Strength (Noisy to Clean)", -2.0, 2.0, 0.5)

if st.sidebar.button("Process Connection Request"):
    # Run the Quantum calculation
    result = quantum_brain(signal_val, learned_weight)
    
    st.subheader(f"Results for {client_name}")
    
    # Logic: If output is positive, Accept. If negative, Reject.
    if result > 0:
        st.success("✅ CONNECTION GRANTED")
        st.info("Reason: Signal quality is above the quantum threshold.")
    else:
        st.error("❌ CONNECTION REJECTED")
        st.warning("Reason: High interference detected. Connection unsafe.")
        
    st.metric(label="Quantum Confidence Score", value=round(float(result), 4))

# Visualizing the process
st.divider()
st.write("### How it works")
st.write("1. **Capture:** The slider simulates raw radio data [Step 1-3 in your diagram].")
st.write("2. **Quantum Logic:** The data is processed via Qubits [Step 5].")
st.write("3. **Action:** The Server updates its ruleset based on the output [Step 6].")