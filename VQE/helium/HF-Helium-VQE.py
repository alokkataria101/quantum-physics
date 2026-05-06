# Helium Hartree-Fock + Ground State Energy (Qiskit Nature)

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
from qiskit_algorithms import NumPyMinimumEigensolver

# Step 1: Define Helium atom
driver = PySCFDriver(
    atom="He 0 0 0",
    basis="sto3g",
    charge=0,
    spin=0,
    unit=DistanceUnit.ANGSTROM
)

# Step 2: Build electronic structure problem
problem = driver.run()

# Step 3: Extract Hartree–Fock energy
hf_energy = problem.reference_energy
print("Hartree–Fock Energy (He):", hf_energy)

# Step 4: Map to qubit Hamiltonian
mapper = JordanWignerMapper()

# Step 5: Solve exactly (Full CI)
solver = GroundStateEigensolver(mapper, NumPyMinimumEigensolver())
result = solver.solve(problem)

print("Exact Ground State Energy:", result.total_energies[0])

# Step 6: Correlation energy
correlation_energy = result.total_energies[0] - hf_energy
print("Correlation Energy:", correlation_energy)
