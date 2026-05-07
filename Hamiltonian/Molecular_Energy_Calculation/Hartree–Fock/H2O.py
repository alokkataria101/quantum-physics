from pyscf import gto, scf

mol = gto.M(
    atom = '''
    O 0 0 0
    H 0 -0.757 0.587
    H 0 0.757 0.587
    ''',
    basis='6-31g'
)

mf = scf.RHF(mol)
energy = mf.kernel()

print("Water molecule energy:", energy)
