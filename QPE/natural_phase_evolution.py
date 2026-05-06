from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

# -----------------------------
# Physical parameters
# -----------------------------
omega = 1.0      # angular frequency (energy scale, ℏ = 1)
t = 2.0          # evolution time

# True values (ground truth)
true_phase = omega * t
true_energy = omega

# -----------------------------
# Build quantum circuit
# -----------------------------
qc = QuantumCircuit(1, 1)

qc.h(0)                     # create superposition
qc.rz(true_phase, 0)        # natural phase from evolution e^{-iHt}
qc.h(0)                     # interference
qc.measure(0, 0)

# -----------------------------
# Run simulation
# -----------------------------
sim = AerSimulator()
shots = 4000

result = sim.run(qc, shots=shots).result()
counts = result.get_counts()

# -----------------------------
# Extract probability
# -----------------------------
p0 = counts.get('0', 0) / shots

# -----------------------------
# Estimate phase from probability
# -----------------------------
# P(0) = cos^2(phi/2)
estimated_phase = 2 * np.arccos(np.sqrt(p0))

# Handle numerical edge cases
estimated_phase = np.real_if_close(estimated_phase)

# -----------------------------
# Estimate energy
# -----------------------------
estimated_energy = estimated_phase / t

# -----------------------------
# Print results
# -----------------------------
print("\n===== INPUT (True Values) =====")
print(f"True Phase (φ)      = {true_phase:.4f}")
print(f"True Energy (E)     = {true_energy:.4f}")

print("\n===== MEASUREMENT =====")
print("Counts              =", counts)
print(f"P(0)                = {p0:.4f}")

print("\n===== ESTIMATED =====")
print(f"Estimated Phase     ≈ {estimated_phase:.4f}")
print(f"Estimated Energy    ≈ {estimated_energy:.4f}")

print("\n===== ERROR =====")
print(f"Phase Error         = {abs(true_phase - estimated_phase):.4f}")
print(f"Energy Error        = {abs(true_energy - estimated_energy):.4f}")
