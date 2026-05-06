from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
from qiskit_algorithms import NumPyMinimumEigensolver  # ✅ fixed

driver = PySCFDriver(
    atom="H 0 0 0; H 0 0 0.735",
    basis="sto3g",
    unit=DistanceUnit.ANGSTROM
)

problem = driver.run()

mapper = JordanWignerMapper()
solver = GroundStateEigensolver(mapper, NumPyMinimumEigensolver())

result = solver.solve(problem)

print("Energy:", result.total_energies[0])
