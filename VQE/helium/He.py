# ===============================
# 1. Imports
# ===============================
import numpy as np

from pyscf import gto, scf

from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Estimator

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.circuit.library import UCCSD
from qiskit_nature.second_q.algorithms import GroundStateEigensolver

# ===============================
# 2. Define Helium Atom
# ===============================
driver = PySCFDriver(
    atom="He 0 0 0",
    basis="sto3g"
)

# Run electronic structure calculation
problem = driver.run()

# ===============================
# 3. Map to Qubits
# ===============================
mapper = JordanWignerMapper()

# ===============================
# 4. Ansatz (UCCSD)
# ===============================
num_particles = problem.num_particles
num_spatial_orbitals = problem.num_spatial_orbitals

ansatz = UCCSD(
    num_spatial_orbitals=num_spatial_orbitals,
    num_particles=num_particles,
    qubit_mapper=mapper
)

# ===============================
# 5. Classical Optimizer
# ===============================
optimizer = COBYLA(maxiter=100)

# ===============================
# 6. Estimator (Simulator backend)
# ===============================
estimator = Estimator()

# ===============================
# 7. VQE Setup
# ===============================
vqe_solver = VQE(
    estimator=estimator,
    ansatz=ansatz,
    optimizer=optimizer
)

# ===============================
# 8. Ground State Solver
# ===============================
calc = GroundStateEigensolver(mapper, vqe_solver)

# ===============================
# 9. Run VQE
# ===============================
result = calc.solve(problem)

# ===============================
# 10. Output
# ===============================
print("Ground State Energy (Hartree):")
print(result.total_energies[0])
