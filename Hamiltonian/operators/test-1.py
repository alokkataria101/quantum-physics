from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit import transpile

qc = QuantumCircuit(3,3)

qc.h(0)
qc.h(1)
qc.cx(0,1)
qc.cx(1,2)

qc.measure([0,1,2],[0,1,2])

backend = Aer.get_backend('aer_simulator')
compiled = transpile(qc, backend)

result = backend.run(compiled, shots=1000).result()
print(result.get_counts())

qc.draw()
