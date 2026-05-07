import numpy as np
import matplotlib.pyplot as plt

from qiskit.primitives import Estimator
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit.circuit.library import TwoLocal

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import ParityMapper
from qiskit_nature.second_q.problems import ElectronicStructureProblem
from qiskit_nature.second_q.transformers import ActiveSpaceTransformer

distances = np.linspace(0.5, 1.5, 10)
energies = []

for d in distances:
    # Step 1: Define molecule at distance d
    driver = PySCFDriver(
        atom=f"H 0 0 0; H 0 0 {d}",
        basis="sto3g"
    )

    problem = ElectronicStructureProblem(driver)

    # Step 2: Reduce to active space
    transformer = ActiveSpaceTransformer(
        num_electrons=2,
        num_spatial_orbitals=2
    )
    problem = transformer.transform(problem)

    # Step 3: Get Hamiltonian
    second_q_ops = problem.second_q_ops()
    main_op = second_q_ops[0]

    mapper = ParityMapper()
    qubit_op = mapper.map(main_op)

    # Step 4: Ansatz
    ansatz = TwoLocal(
        rotation_blocks="ry",
        entanglement_blocks="cz",
        reps=2
    )

    # Step 5: Optimizer + Estimator
    optimizer = SLSQP(maxiter=100)
    estimator = Estimator()

    vqe = VQE(estimator, ansatz, optimizer)

    # Step 6: Run VQE
    result = vqe.compute_minimum_eigenvalue(qubit_op)
    energy = result.eigenvalue.real

    print(f"Distance: {d:.2f} Å → Energy: {energy:.5f}")

    energies.append(energy)

# Step 7: Find minimum
min_energy = min(energies)
optimal_distance = distances[energies.index(min_energy)]

print("\nOptimal bond length (VQE):", optimal_distance)

# Step 8: Plot
plt.plot(distances, energies, marker='o')
plt.xlabel("Bond distance (Å)")
plt.ylabel("Energy (Hartree)")
plt.title("H2 Energy vs Bond Length (VQE)")
plt.show()
