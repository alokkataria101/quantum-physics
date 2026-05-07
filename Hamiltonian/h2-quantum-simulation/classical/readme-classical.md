# Classical Simulation of H₂ Molecule

## Overview
This project computes the ground state energy of the hydrogen molecule (H₂) using classical quantum chemistry methods.

The goal is to determine:
- Ground state energy
- Equilibrium bond length (≈ 0.735 Å)

---

## Core Idea

We solve the time-independent Schrödinger equation:

Hψ = Eψ

Where:
- H = Hamiltonian (energy operator)
- ψ = wavefunction
- E = energy

---

## Method Used

### 1. Basis Set Approximation
- Continuous electron behavior is approximated using basis functions
- Example: STO-3G

---

### 2. Hamiltonian Construction
- Includes:
  - Electron kinetic energy
  - Electron-nucleus attraction
  - Electron-electron repulsion

---

### 3. Hartree-Fock (HF) Method
- Approximates many-electron wavefunction
- Uses iterative self-consistent field (SCF) approach

---

### 4. Bond Length Optimization
- Energy is computed for different distances
- The minimum energy point gives equilibrium bond length

---

## Workflow

1. Define molecule geometry
2. Choose basis set
3. Run SCF (Hartree-Fock)
4. Compute energy
5. Repeat for multiple bond distances
6. Find minimum energy

---

## Example (PySCF)

```python
from pyscf import gto, scf

mol = gto.M(
    atom='H 0 0 0; H 0 0 0.735',
    basis='sto-3g'
)

mf = scf.RHF(mol)
energy = mf.kernel()

print("Ground state energy:", energy)
