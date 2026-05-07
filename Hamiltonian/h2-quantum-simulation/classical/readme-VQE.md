
---

# 📄 `readme-VQE.md`

```markdown
# Quantum Simulation of H₂ using VQE

## Overview
This project computes the ground state energy of the hydrogen molecule (H₂) using a hybrid quantum-classical algorithm called Variational Quantum Eigensolver (VQE).

---

## Core Idea

We estimate energy using:

E(θ) = ⟨ψ(θ)|H|ψ(θ)⟩

Where:
- H = Hamiltonian (mapped to qubits)
- ψ(θ) = parameterized quantum state
- θ = tunable parameters

---

## Method Used

### 1. Problem Mapping
- Molecular Hamiltonian is converted into qubit operators
- Uses transformations like Parity mapping

---

### 2. Ansatz (Trial Circuit)
- Parameterized quantum circuit
- Example: TwoLocal (RY rotations + entanglement)

---

### 3. Hybrid Optimization Loop

1. Prepare quantum state
2. Measure energy
3. Update parameters using classical optimizer
4. Repeat until minimum energy is found

---

### 4. Bond Length Optimization
- Run VQE for multiple bond distances
- Find distance where energy is minimum (~0.735 Å)

---

## Workflow

1. Define molecule geometry
2. Build Hamiltonian
3. Map to qubits
4. Choose ansatz
5. Run VQE
6. Repeat for different bond lengths
7. Find minimum energy

---

## Example (Qiskit)

```python
from qiskit.primitives import Estimator
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit.circuit.library import TwoLocal

# Define ansatz
ansatz = TwoLocal(
    rotation_blocks="ry",
    entanglement_blocks="cz",
    reps=2
)

optimizer = SLSQP()
estimator = Estimator()

vqe = VQE(estimator, ansatz, optimizer)
result = vqe.compute_minimum_eigenvalue(qubit_op)

print("Ground state energy:", result.eigenvalue.real)
