import numpy as np
from pyscf import gto, scf

distances = np.linspace(0.5, 1.5, 10)
energies = []

for d in distances:
    mol = gto.M(
        atom=f'H 0 0 0; H 0 0 {d}',
        basis='sto-3g'
    )
    mf = scf.RHF(mol)
    energy = mf.kernel()
    energies.append(energy)

# Find minimum
min_energy = min(energies)
optimal_distance = distances[energies.index(min_energy)]

print("Optimal bond length:", optimal_distance)
