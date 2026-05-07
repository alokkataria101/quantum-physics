import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
from scipy.constants import physical_constants

# ================================================================
# PARAMETERS (Atomic units: ħ = m = e = 1)
# ================================================================
hartree_to_eV = physical_constants['Hartree energy in eV'][0]

r_max = 50.0    # Max radius in Bohr (a0)
N = 10000        # Number of grid points
r = np.linspace(0, r_max, N)

# Avoid singularity — enforce u(0) = 0 by starting computation from r = dr
dr = r[1] - r[0]
r[0] = dr

# ================================================================
# CONSTRUCT THE HAMILTONIAN H = -1/2 d2/dr2 + V(r)
# ================================================================

# Kinetic term (-1/2 d2/dr2)
main_diag = np.full(N, -2.0) / (dr**2)
off_diag = np.full(N-1, 1.0) / (dr**2)
lap = diags([off_diag, main_diag, off_diag], offsets=[-1, 0, 1], format='csr')
T = -0.5 * lap

# Coulomb potential V(r) = -1/r
V = -1.0 / r
V_matrix = diags(V, 0, format='csr')

# Hamiltonian
H = T + V_matrix

# ================================================================
# SOLVE FOR LOWEST EIGENVALUES
# ================================================================
k = 5  # number of eigenvalues to compute
eigvals, eigvecs = eigsh(H, k=k, which='SA')

# Sort eigenvalues
idx = np.argsort(eigvals)
eigvals = eigvals[idx]
eigvecs = eigvecs[:, idx]

# Ground state energy (first)
E0_hartree = eigvals[0]
E0_eV = E0_hartree * hartree_to_eV

print(f"\nNumerical ground state energy: {E0_hartree:.8f} Hartree = {E0_eV:.6f} eV")
print("Analytical exact value:       -0.500000 Hartree = -13.605693 eV\n")

# ================================================================
# NORMALIZE u(r) AND COMPUTE R(r)
# ================================================================
u = eigvecs[:, 0]
norm = np.sqrt(np.trapz(np.abs(u)**2, r))
u = u / norm
R = u / r

# ================================================================
# PLOTTING
# ================================================================
plt.figure(figsize=(12,4))

plt.subplot(1,2,1)
plt.plot(r, u)
plt.title("u(r) = r R(r) (Radial Function)")
plt.xlabel("r (Bohr)")
plt.ylabel("u(r)")
plt.grid(True)

plt.subplot(1,2,2)
plt.plot(r, np.abs(R)**2)
plt.title("Radial Probability Density |R(r)|²")
plt.xlabel("r (Bohr)")
plt.ylabel("|R(r)|²")
plt.grid(True)

plt.tight_layout()
plt.show()


