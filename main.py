import pennylane as qml
from pennylane import numpy as np
import matplotlib.pyplot as plt

# We use a 2-qubit simulator
dev = qml.device("default.qubit", wires=2)

@qml.qnode(dev)
def qnn_circuit(inputs, weights):
    # inputs[0] is the signal amplitude
    qml.RY(inputs[0], wires=0)
    qml.RY(inputs[0], wires=1)
    # We use basic rotation gates with weights that the optimizer will tune
    qml.RX(weights[0], wires=0)
    qml.RX(weights[1], wires=1)
    qml.CNOT(wires=[0, 1]) 
    return qml.expval(qml.PauliZ(0))

def generate_data(n_samples=100):
    # Binary bits: -1 (for bit 0) and 1 (for bit 1)
    X = np.random.choice([-1, 1], n_samples)
    # Add Gaussian Noise (Simulating a noisy wireless channel)
    noise = np.random.normal(0, 0.5, n_samples)
    X_noisy = X + noise
    # Labels: 0 for -1, 1 for +1
    Y = np.where(X < 0, -1, 1)
    return X_noisy.reshape(-1, 1), Y

def cost(weights, X, Y):
    predictions = [qnn_circuit(x, weights) for x in X]
    return np.mean((np.array(predictions) - Y)**2)
# Initialize data and weights
X_train, Y_train = generate_data(40)
weights = np.array([0.1, 0.1], requires_grad=True)
# Use the Adam Optimizer (Hybrid Loop)
opt = qml.AdamOptimizer(stepsize=0.1)
print("Starting Training...")
for i in range(20):
    weights, current_cost = opt.step_and_cost(cost, weights, X=X_train, Y=Y_train)
    if i % 5 == 0:
        print(f"Epoch {i} | Cost: {current_cost:.4f}")

# --- 5. VISUALIZE RESULTS ---
print("\nFinal Learned Weights:", weights)

# Test on new data
X_test, Y_test = generate_data(10)
preds = [1 if qnn_circuit(x, weights) > 0 else -1 for x in X_test]
print(f"Test Accuracy: {np.mean(preds == Y_test) * 100}%")





"""# ==========================================
# STEP 1 & 2: WIRELESS NETWORK & SERVER 
# (Simulating Client connection attempts)
# ==========================================
import pennylane as qml
from pennylane import numpy as np

def simulate_wireless_network(n_clients=50):
    # '1' represents a valid user, '-1' represents a malicious/noisy user
    client_signals = np.random.choice([-1, 1], n_clients)
    noise = np.random.normal(0, 0.4, n_clients) # Channel interference
    return client_signals + noise, client_signals

# ==========================================
# STEP 3: SAVE RELEVANT CONNECTIVITY DATA
# ==========================================
X_connectivity_data, Y_labels = simulate_wireless_network()

# ==========================================
# STEP 4 & 5: QUANTUM MODEL TRAINING & DEPLOY
# ==========================================
dev = qml.device("default.qubit", wires=1) # The Quantum Processor

@qml.qnode(dev)
def quantum_neural_network(data, weights):
    # Mapping data to Quantum State (Hilbert Space)
    qml.RY(data, wires=0) 
    # The 'Brain': Parameterized Quantum Gate
    qml.RX(weights, wires=0) 
    return qml.expval(qml.PauliZ(0))

# Training Logic (The Hybrid Loop)
def train_model(X, Y):
    weights = np.array(0.1, requires_grad=True)
    opt = qml.AdamOptimizer(stepsize=0.1)
    
    for _ in range(30): # 30 Training iterations
        weights = opt.step(lambda w: np.mean((np.array([quantum_neural_network(x, w) for x in X]) - Y)**2), weights)
    return weights

# ==========================================
# STEP 6: MODEL PROVIDES LEARNED PARAMETERS
# ==========================================
final_ruleset_weights = train_model(X_connectivity_data, Y_labels)

def server_decision(new_signal):
    # Deployment: Server accepts/rejects based on QNN output
    prediction = quantum_neural_network(new_signal, final_ruleset_weights)
    return "ACCEPT" if prediction > 0 else "REJECT"

# Example Deployment
print(f"Decision for Client Signal 0.8: {server_decision(0.8)}")"""