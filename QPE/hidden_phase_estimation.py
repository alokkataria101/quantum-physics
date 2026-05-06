from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

sim = AerSimulator()

def measure_phase(phi, shots=2000):
    qc = QuantumCircuit(1, 1)

    qc.h(0)         # create superposition
    qc.p(phi, 0)    # hidden phase
    qc.h(0)         # convert phase → probability
    qc.measure(0, 0)

    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()

    p0 = counts.get('0', 0) / shots

    # Recover phase
    estimated_phi = 2 * np.arccos(np.sqrt(p0))

    return counts, estimated_phi


# Try unknown phases
hidden_phases = [0.3, 1.0, 2.2]

for phi in hidden_phases:
    counts, est = measure_phase(phi)

    print(f"\nActual φ = {phi:.3f}")
    print(f"Estimated φ ≈ {est:.3f}")
    print("Counts:", counts)
