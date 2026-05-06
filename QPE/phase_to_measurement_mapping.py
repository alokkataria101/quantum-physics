from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

phi = np.pi / 2

qc = QuantumCircuit(1, 1)

qc.h(0)
qc.p(phi, 0)
qc.h(0)
qc.measure(0, 0)

sim = AerSimulator()
result = sim.run(qc, shots=1000).result()
counts = result.get_counts()

print("Phase (phi):", phi)
print("Counts:", counts)
