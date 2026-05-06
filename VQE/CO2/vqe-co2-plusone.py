# ===============================
# 1. Imports
# ===============================
import numpy as np

from qiskit.primitives import Estimator
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.transformers import ActiveSpaceTransformer
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.circuit.library import UCCSD
from qiskit_nature.second_q.algorithms import GroundStateEigensolver

# ===============================
# 2. Define CO2 geometry
# ===============================

driver = PySCFDriver(
    atom="O 0 0 -1.16; C 0 0 0; O 0 0 1.16",
    basis="sto3g",
    charge=1,
    spin=1   # ✅ REQUIRED
)
problem = driver.run()

# ===============================
# 3. Active Space Reduction
# ===============================
# Reduce problem size
transformer = ActiveSpaceTransformer(
    num_electrons=4,            # choose valence electrons
    num_spatial_orbitals=4      # small active space
)

reduced_problem = transformer.transform(problem)

# ===============================
# 4. Qubit Mapping
# ===============================
mapper = JordanWignerMapper()

# ===============================
# 5. Ansatz
# ===============================
num_particles = reduced_problem.num_particles
num_spatial_orbitals = reduced_problem.num_spatial_orbitals

ansatz = UCCSD(
    num_spatial_orbitals=num_spatial_orbitals,
    num_particles=num_particles,
    qubit_mapper=mapper
)

# ===============================
# 6. Optimizer
# ===============================
optimizer = COBYLA(maxiter=200)

# ===============================
# 7. Estimator
# ===============================
estimator = Estimator()

# ===============================
# 8. VQE Setup
# ===============================
vqe = VQE(
    estimator=estimator,
    ansatz=ansatz,
    optimizer=optimizer
)

# ===============================
# 9. Solve Ground State
# ===============================
solver = GroundStateEigensolver(mapper, vqe)

result = solver.solve(reduced_problem)

# ===============================
# 10. Output
# ===============================
print("CO2 Ground State Energy (Hartree):")
print(result.total_energies[0])
