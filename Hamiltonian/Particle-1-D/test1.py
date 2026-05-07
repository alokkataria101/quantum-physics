import numpy as np
from scipy.constants import hbar, m_e, eV
from scipy.linalg import eigh

H = [
    [-5,-7],
    [2,4]
]

# Solve Schrödinger equation
eigvals, eigvecs = eigh(H)

# Print first few bound-state energies (negative energies)
print(f"{eigvals} {eigvecs}")

