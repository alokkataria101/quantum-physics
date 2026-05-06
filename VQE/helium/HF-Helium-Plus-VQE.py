# He+ (Helium ion) Hartree-Fock + Exact Energy

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
from qiskit_algorithms import NumPyMinimumEigensolver

# Step 1: Define He+ (1 electron removed)
driver = PySCFDriver(
    atom="He 0 0 0",
    basis="sto3g",
    charge=+1,   # <-- KEY difference from He
    spin=1,      # 2S = 1 → one unpaired electron
    unit=DistanceUnit.ANGSTROM
)

# Step 2: Build problem
problem = driver.run()

# Step 3: Hartree–Fock energy
hf_energy = problem.reference_energy
print("Hartree–Fock Energy (He+):", hf_energy)

# Step 4: Qubit mapping
mapper = JordanWignerMapper()

# Step 5: Exact solver (FCI)
solver = GroundStateEigensolver(mapper, NumPyMinimumEigensolver())
result = solver.solve(problem)

print("Exact Ground State Energy:", result.total_energies[0])

# Step 6: Correlation energy
correlation_energy = result.total_energies[0] - hf_energy
print("Correlation Energy:", correlation_energy)
