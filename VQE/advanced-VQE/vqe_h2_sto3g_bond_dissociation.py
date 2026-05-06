import numpy as np

# Qiskit primitives & circuits
from qiskit.primitives import Estimator
from qiskit.circuit.library import TwoLocal

# Algorithms (separate package)
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP

# Qiskit Nature
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper


# ---------------------------
# Compute VQE Energy
# ---------------------------
def compute_vqe_energy(molecule, charge=0, spin=0):
    """
    molecule: string like "H 0 0 0; H 0 0 0.74"
    spin = N_alpha - N_beta (NOT 2S+1)
    """

    # Step 1: Define system
    driver = PySCFDriver(
        atom=molecule,
        basis="sto3g",
        charge=charge,
        spin=spin
    )

    # Step 2: Run electronic structure
    problem = driver.run()

    # Step 3: Get Hamiltonian
    second_q_ops = problem.second_q_ops()
    hamiltonian = second_q_ops[0]

    # Step 4: Map to qubit operator
    mapper = JordanWignerMapper()
    qubit_op = mapper.map(hamiltonian)

    # Step 5: Ansatz
    ansatz = TwoLocal(
        qubit_op.num_qubits,
        rotation_blocks="ry",
        entanglement_blocks="cz",
        reps=2
    )

    # Step 6: Optimizer & Estimator
    optimizer = SLSQP(maxiter=200)
    estimator = Estimator()

    # Step 7: VQE
    vqe = VQE(estimator, ansatz, optimizer)
    result = vqe.compute_minimum_eigenvalue(qubit_op)

    return result.eigenvalue.real


# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":

    print("\n===== Running VQE for H2 =====")

    # H2 (closed shell → spin=0)
    E_H2 = compute_vqe_energy(
        "H 0 0 0; H 0 0 0.74",
        spin=0
    )

    # H atom (open shell → spin=1)
    E_H = compute_vqe_energy(
        "H 0 0 0",
        spin=1
    )

    # Bond Dissociation Energy
    BDE_hartree = 2 * E_H - E_H2

    # Convert to kJ/mol
    hartree_to_kj = 2625.5
    BDE_kj = BDE_hartree * hartree_to_kj

    print("\n===== Results =====")
    print(f"E(H2) = {E_H2:.6f} Hartree")
    print(f"E(H)  = {E_H:.6f} Hartree")
    print(f"BDE   = {BDE_kj:.2f} kJ/mol")

    # Experimental comparison
    experimental_bde = 436  # kJ/mol

    print("\n===== Comparison =====")
    print(f"Experimental BDE ≈ {experimental_bde} kJ/mol")
    print(f"Error ≈ {abs(BDE_kj - experimental_bde):.2f} kJ/mol")
