# LiH Ionization Potential using Qiskit Nature

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.units import DistanceUnit

# ---------------------------
# Step 1: Neutral LiH
# ---------------------------
driver_LiH = PySCFDriver(
    atom="Li 0 0 0; H 0 0 1.6",   # bond length ~1.6 Å
    basis="sto3g",
    charge=0,
    spin=0,
    unit=DistanceUnit.ANGSTROM
)

problem_LiH = driver_LiH.run()
E_LiH = problem_LiH.reference_energy  # Hartree–Fock energy

print("HF Energy (LiH):", E_LiH)


# ---------------------------
# Step 2: Ionized LiH+
# ---------------------------
driver_LiH_plus = PySCFDriver(
    atom="Li 0 0 0; H 0 0 1.6",
    basis="sto3g",
    charge=+1,   # remove one electron
    spin=1,      # unpaired electron
    unit=DistanceUnit.ANGSTROM
)

problem_LiH_plus = driver_LiH_plus.run()
E_LiH_plus = problem_LiH_plus.reference_energy

print("HF Energy (LiH+):", E_LiH_plus)


# ---------------------------
# Step 3: Ionization Potential
# ---------------------------
IP_hartree = E_LiH_plus - E_LiH

# Convert Hartree → eV
IP_eV = IP_hartree * 27.2114

print("\nIonization Potential:")
print("IP (Hartree):", IP_hartree)
print("IP (eV):", IP_eV)
