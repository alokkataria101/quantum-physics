# H₂ Simulation: Classical vs Quantum (VQE)

This project demonstrates how to compute the ground state energy of the hydrogen molecule using:

- Classical Hartree-Fock (PySCF)
- Quantum VQE (Qiskit)

It also compares both approaches and shows how equilibrium bond length (~0.735 Å) emerges from energy minimization.

---

## Run

### Classical
cd classical
python h2_classical.py

### Quantum (VQE)
cd vqe
python h2_vqe_scan.py
