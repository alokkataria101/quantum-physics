# CCSD Reaction Energy: C + O2 -> CO2

from pyscf import gto, scf, cc

def compute_ccsd_energy(atom_string, spin, charge=0, basis="cc-pvdz"):
    mol = gto.M(
        atom=atom_string,
        basis=basis,
        spin=spin,
        charge=charge,
        unit="Angstrom"
    )
    
    # Hartree-Fock
    mf = scf.RHF(mol) if spin == 0 else scf.UHF(mol)
    mf.kernel()
    
    # CCSD
    mycc = cc.CCSD(mf)
    mycc.kernel()
    
    return mycc.e_tot


# ---------------------------
# Carbon atom (triplet)
# ---------------------------
E_C = compute_ccsd_energy("C 0 0 0", spin=2)

# ---------------------------
# O2 (triplet)
# ---------------------------
E_O2 = compute_ccsd_energy("O 0 0 0; O 0 0 1.21", spin=2)

# ---------------------------
# CO2 (singlet, linear)
# ---------------------------
E_CO2 = compute_ccsd_energy(
    "C 0 0 0; O 0 0 1.16; O 0 0 -1.16",
    spin=0
)

# ---------------------------
# Reaction energy
# ---------------------------
deltaE_hartree = (E_C + E_O2) - E_CO2
deltaE_eV = deltaE_hartree * 27.2114

print("Reaction Energy (Hartree):", deltaE_hartree)
print("Reaction Energy (eV):", deltaE_eV)
