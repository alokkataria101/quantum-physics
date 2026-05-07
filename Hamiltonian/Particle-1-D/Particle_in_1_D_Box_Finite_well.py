import numpy as np
from scipy.constants import hbar, m_e, eV
from scipy.linalg import eigh

# Parameters
L = 1e-9             # 1 nm
N = 600              # grid points
m = m_e              # electron mass

V0 = 0.5 * eV        # finite well height (0.5 eV)
well_width = 0.5e-9  # central well = 0.5 nm

# Grid
x = np.linspace(0, L, N)
dx = x[1] - x[0]

# Define finite square well
V = np.zeros(N)
center = L/2
for i in range(N):
    if abs(x[i] - center) > well_width/2:
        V[i] = V0
    else:
        V[i] = 0

# Kinetic-energy matrix
coeff = -hbar**2 / (2*m*dx**2)
H = np.zeros((N, N))

for i in range(N):
    H[i, i] = -2
    if i > 0:
        H[i, i-1] = 1
    if i < N-1:
        H[i, i+1] = 1

H = coeff * H

# Add potential V(x)
for i in range(N):
    H[i, i] += V[i]

# Solve Schrödinger equation
eigvals, eigvecs = eigh(H)

# Convert to eV
energies_eV = eigvals / eV

# Print first few bound-state energies (negative energies)
print("Bound state energies (eV):")
for E in energies_eV[:10]:
    if E < V0/eV:        # inside well
        print(E)

