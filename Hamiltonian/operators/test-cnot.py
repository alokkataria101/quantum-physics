from qiskit import QuantumCircuit

qc = QuantumCircuit(2,2)

qc.h(0)        # Hadamard on qubit 0
qc.cx(0,1)     # CNOT
qc.measure([0,1],[0,1])

print(qc)
